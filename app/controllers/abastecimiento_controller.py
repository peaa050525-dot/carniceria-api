from app.models.abastecimiento_model import AbastecimientoModel
from app.views.abastecimiento_view import AbastecimientoView

class AbastecimientoController:
    def __init__(self, parent_notebook):
        self.modelo = AbastecimientoModel()
        self.vista = AbastecimientoView(parent_notebook)
        
        # Escuchar cuando se agregue un nuevo abastecimiento desde el otro módulo
        parent_notebook.bind_all("<<NuevoAbastecimiento>>", lambda e: self.cargar_historial())
        
        self.cargar_historial()

    def cargar_historial(self):
        registros = self.modelo.obtener_historial_db()
        self.vista.actualizar_tabla(registros)