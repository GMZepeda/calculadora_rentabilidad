from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# SUB-NODO A: VALIDACIÓN (Definimos qué datos esperamos recibir y que sean números)
class DatosProducto(BaseModel):
    precio: float
    costo: float
    impuesto_porcentaje: float

@app.post("/calcular")
def calcular_rentabilidad(datos: DatosProducto):
    
    # SUB-NODO A: VALIDACIÓN DE NEGOCIO (Evitar valores negativos o absurdos)
    if datos.precio <= 0 or datos.costo < 0 or datos.impuesto_porcentaje < 0:
        raise HTTPException(status_code=400, detail="Los valores no pueden ser negativos y el precio debe ser mayor a cero.")
    
    # SUB-NODO B: CÁLCULO (Motor matemático)
    costo_impuesto = datos.precio * (datos.impuesto_porcentaje / 100)
    ganancia_neta = datos.precio - datos.costo - costo_impuesto
    margen = (ganancia_neta / datos.precio) * 100
    
    # SUB-NODO C: FORMATEO (Redondear a 2 decimales y agregar signos)
    ganancia_formateada = round(ganancia_neta, 2)
    margen_formateado = round(margen, 2)
    
    return {
        "ganancia_neta": f"${ganancia_formateada}",
        "margen": f"{margen_formateado}%"
    }