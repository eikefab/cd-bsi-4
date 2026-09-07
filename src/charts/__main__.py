from . import generate_charts


if __name__ == "__main__":
    for arquivo in generate_charts():
        print(f"Gráfico salvo em: {arquivo}")
