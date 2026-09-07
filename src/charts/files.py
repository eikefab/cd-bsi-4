import matplotlib.pyplot as plt


def salva_grafico(fig, output_folder, nome):
    arquivo = output_folder / nome
    if not fig.get_constrained_layout():
        fig.tight_layout()
    try:
        fig.savefig(arquivo, dpi=150, bbox_inches="tight")
    finally:
        plt.close(fig)
    return arquivo

