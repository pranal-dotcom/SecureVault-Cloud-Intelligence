import io
import logging
from typing import Optional, List, Any

# Safe imports for OCR and PDF engines
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    Image = None  # type: ignore
    PIL_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None  # type: ignore
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None  # type: ignore
    PYTESSERACT_AVAILABLE = False

logger = logging.getLogger("securevault.ai.ocr")


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an image (PNG, JPEG, WEBP, TIFF, BMP) using Tesseract OCR.
    """
    if not PIL_AVAILABLE or Image is None:
        raise ValueError("PIL (Pillow) library is required for image processing. Please ensure pillow is installed.")

    if not PYTESSERACT_AVAILABLE or pytesseract is None:
        raise ValueError("pytesseract library is required for image OCR. Please ensure pytesseract is installed.")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if necessary (e.g. RGBA or palette modes)
        if getattr(image, "mode", "") not in ("L", "RGB"):
            image = image.convert("RGB")
        
        extracted = pytesseract.image_to_string(image)
        return str(extracted).strip() if extracted else ""
    except Exception as e:
        err_msg = str(e)
        if "tesseract is not installed or it's not in your PATH" in err_msg.lower() or "not found" in err_msg.lower():
            logger.warning("Tesseract OCR engine binary not found on local system path.")
            raise ValueError(
                "Tesseract OCR binary is not installed on this host system. "
                "For scanned image OCR, install Tesseract-OCR or run via the containerized Docker service. "
                "Native PDF text extraction and raw text processing remain fully operational."
            )
        logger.error(f"Error during image OCR extraction: {err_msg}")
        raise ValueError(f"Failed to process image OCR: {err_msg}")


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts clean text from a PDF file using pdfplumber, falling back
    to image OCR on scanned pages if native text is sparse.
    """
    if not PDFPLUMBER_AVAILABLE or pdfplumber is None:
        raise ValueError("pdfplumber library is required for PDF parsing. Please ensure pdfplumber is installed.")

    extracted_text_chunks: List[str] = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                
                # If native text is very short (scanned PDF), try image OCR on page image if available
                page_images: Any = getattr(page, "images", [])
                if len(page_text.strip()) < 20 and len(page_images) > 0 and PYTESSERACT_AVAILABLE and pytesseract is not None:
                    try:
                        page_img_wrapper = page.to_image(resolution=200)
                        page_img = getattr(page_img_wrapper, "original", None)
                        if page_img is not None:
                            ocr_text = str(pytesseract.image_to_string(page_img)).strip()
                            if len(ocr_text) > len(page_text.strip()):
                                page_text = ocr_text
                    except Exception as ocr_err:
                        logger.warning(f"OCR fallback skipped on page {page_num}: {ocr_err}")
                
                if page_text.strip():
                    extracted_text_chunks.append(page_text.strip())
                    
        return "\n\n".join(extracted_text_chunks).strip()
    except Exception as e:
        logger.error(f"Error during PDF text extraction: {e}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def process_document_ocr(file_bytes: bytes, filename: str, content_type: Optional[str] = None) -> str:
    """
    Auto-detects document format (PDF vs Image vs Text) and executes appropriate extraction pipeline.
    """
    filename_lower = filename.lower()
    
    # 1. PDF Processing
    if filename_lower.endswith(".pdf") or (content_type and "pdf" in content_type.lower()):
        return extract_text_from_pdf(file_bytes)
    
    # 2. Image Processing
    image_exts = (".png", ".jpg", ".jpeg", ".webp", ".tiff", ".tif", ".bmp")
    if filename_lower.endswith(image_exts) or (content_type and content_type.startswith("image/")):
        return extract_text_from_image(file_bytes)
    
    # 3. Direct UTF-8 Text File Fallback
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Try image OCR as last resort
        try:
            return extract_text_from_image(file_bytes)
        except Exception:
            raise ValueError(
                f"Unsupported file format for '{filename}'. Supported formats: PDF, PNG, JPG, WEBP, BMP, TIFF, TXT."
            )
