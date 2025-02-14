import pickle  # Para guardar y cargar datos en un archivo
import os      # Para manejar archivos en el sistema

CHECKPOINT_ARCHIVO = "checkpoint.pkl"  # Archivo donde se guarda la última página leída
LIBROS_DIR = "libros"  # Carpeta donde se encuentran los libros

def save_checkpoint(book_name, page):
    """Guarda la última página leída de un libro específico."""
    checkpoints = load_all_checkpoints()
    checkpoints[book_name] = page  # Guarda la página del libro actual
    with open(CHECKPOINT_ARCHIVO, "wb") as archivo:
        pickle.dump(checkpoints, archivo)  # Guarda el diccionario con checkpoints

def load_checkpoint(book_name):
    """Carga la última página leída de un libro específico."""
    checkpoints = load_all_checkpoints()
    return checkpoints.get(book_name, 0)  # Devuelve la página guardada o 0 si no existe

def load_all_checkpoints():
    """Carga todos los checkpoints guardados."""
    if os.path.exists(CHECKPOINT_ARCHIVO):
        with open(CHECKPOINT_ARCHIVO, "rb") as f:
            return pickle.load(f)  # Carga el diccionario de checkpoints
    return {}  # Si no existe, devuelve un diccionario vacío

def get_books():
    """Lista los libros disponibles en la carpeta 'libros'."""
    if not os.path.exists(LIBROS_DIR):
        os.makedirs(LIBROS_DIR)  # Crea la carpeta si no existe
    return [f for f in os.listdir(LIBROS_DIR) if f.endswith(".txt")]

def load_book(book_name):
    """Carga el contenido de un libro en forma de lista de líneas."""
    book_path = os.path.join(LIBROS_DIR, book_name)
    if os.path.exists(book_path):
        with open(book_path, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def read_book():
    """Permite al usuario elegir y leer un libro con guardado de progreso."""
    books = get_books()
    if not books:
        print("No hay libros disponibles en la carpeta 'libros'. Agrega archivos .txt y vuelve a intentarlo.")
        return
    
    # Mostrar libros disponibles
    print("Libros disponibles:")
    for idx, book in enumerate(books, start=1):
        print(f"{idx}. {book}")
    
    # Seleccionar un libro
    while True:
        try:
            choice = int(input("Elige un libro ingresando su número: ")) - 1
            if 0 <= choice < len(books):
                book_name = books[choice]
                break
            else:
                print("Número fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Ingresa un número.")
    
    book = load_book(book_name)
    if not book:
        print("No se pudo cargar el libro.")
        return
    
    last_page = load_checkpoint(book_name)
    print(f"\nContinuando desde la página {last_page + 1}\n")
    
    for i in range(last_page, len(book)):
        print(f"Página {i + 1}:")
        print(book[i])
        input("Presiona Enter para continuar...")
        save_checkpoint(book_name, i + 1)
    
    print("¡Has terminado el libro!")
    save_checkpoint(book_name, 0)  # Reinicia el checkpoint cuando termina

if __name__ == "__main__":
    read_book()
