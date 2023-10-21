# Este método formatea las cantidades separando los miles por comas y los flotantes con un punto.
# El métdoo devuelve texto.
@staticmethod
def formato_flotantes(cantidad) -> str:
    return "{:,.2f}".format(cantidad)