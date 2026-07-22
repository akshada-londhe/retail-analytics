from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    """Check if file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_upload(file):
    """
    Validate uploaded file.

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"

    if file.filename == '':
        return False, "No filename"

    if not allowed_file(file.filename):
        return False, "Only CSV files allowed"

    return True, None


def get_safe_filename(filename):
    """Get safe filename."""
    return secure_filename(filename)
