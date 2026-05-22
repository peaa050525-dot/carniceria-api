import threading

def ejecutar_en_hilo(tarea_target, args=(), on_success=None, on_error=None):
 
    def worker():
        try:
            
            resultado = tarea_target(*args)
            
            
            if on_success:
                on_success(resultado)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                print(f"Error en hilo: {e}")

    hilo = threading.Thread(target=worker, daemon=True)
    hilo.start()