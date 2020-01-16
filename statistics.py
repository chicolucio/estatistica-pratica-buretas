import pandas as pd
import numpy as np
from matplotlib.lines import Line2D


def freq_table(values,
               bin_min,
               bin_max,
               bin_width,
               count_name='Count',
               bins_name='Bins',
               count_p_name='Count / %',
               count_cum_name='Cumulative count',
               count_p_cum_name='Cumulative count / %'):
    """Função para criar tabela de frequências. Recebe os valores, o mínimo,
    o máximo, e a largura do bin. Retorna dataframe com contagem e percentagem
    de valores em cada bin, tanto absolutas quanto cumulativas

    Parameters
    ----------
    values : array
        Sequência de valores. Pode ser uma série de um Pandas DataFrame
    bin_min : float
        Valor mínimo a ser considerado.
    bin_max : float
        Valor máximo a ser considerado.
    bin_width : float
        Intervalo de bins a ser considerado
    count_name : str, optional
        Nome da coluna de contagem, by default 'Count'
    bins_name : str, optional
        Nome da coluna de bins, by default 'Bins'
    count_p_name : str, optional
        Nome da coluna de contagem em %, by default 'Count / %'
    count_cum_name : str, optional
        Nome da coluna de contagem cumulativa, by default 'Cumulative count'
    count_p_cum_name : str, optional
        Nome da coluna de contagem em % cumulativa, by default
        'Cumulative count / %'

    Returns
    -------
    Pandas DataFrame
        DataFrame com a tabela de frequências.
    """

    bins_tab = pd.DataFrame(
        values.rename(count_name).groupby(
            pd.cut(values.rename(bins_name),
                   np.arange(bin_min, bin_max, bin_width),
                   right=False)).count())

    bins_tab[count_p_name] = round(
        100 * bins_tab[count_name] / bins_tab[count_name].sum(), 2)

    bins_tab[count_cum_name] = bins_tab[count_name].cumsum()
    bins_tab[count_p_cum_name] = bins_tab[count_p_name].cumsum()

    return bins_tab


# As configurações abaixo são para possibilitar mostrar os números nos gráficos
# com vírgulas ao invés de pontos, como é usual no Brasil. Como é comum a
# língua inglesa em programação e publicações, recomendo que se acostumem com
# formatos em inglês.

# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# É necessário também descomentar uma das linhas da função plot_param


def plot_param(ax=None):
    """Função auxiliar. Padroniza o grid e os ticks dos gráficos.

    Parameters
    ----------
    ax : Matplotlib Axes, optional
        Eixos nos quais serão aplicados os parâmetros, by default None
    """
    ax.minorticks_on()
    ax.grid(b=True, which='major', linestyle=':', linewidth=1.0)
    ax.tick_params(which='both', labelsize=14)
    ax.grid(b=True, which='minor', linestyle=':', linewidth=1.0, axis='x')
    ax.tick_params(which='both', labelsize=14)
    ax.tick_params(which='major', length=6)
    ax.tick_params(which='minor', length=3)
    ax.tick_params(which='minor', axis='y', left=False)
#     plt.rcParams['axes.formatter.use_locale'] = True  # usar se quiser
#     formato de números com vírgula.


def plot_hist(values, bin_min, bin_max, bin_width, ax=None, outlier=False):
    """Plot de histograma

    Parameters
    ----------
    values : array
        Sequência de valores. Pode ser uma série de um Pandas DataFrame
    bin_min : float
        Valor mínimo a ser considerado.
    bin_max : float
        Valor máximo a ser considerado.
    bin_width : float
        Intervalo de bins a ser considerado
    ax : Matplotlib Axes, optional
        Eixos nos quais serão aplicados os parâmetros, by default None
    outlier : bool, optional
        Se os outliers devem ser exibidos na legenda, by default False
    """
    plot_param(ax)
    bins = np.arange(bin_min, bin_max, bin_width)
    ax.hist(values,
            bins,
            align='mid',
            facecolor='g',
            alpha=0.6,
            edgecolor='k',
            label='')

    ax.set_xticks(np.arange(bin_min, bin_max, bin_width))

    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    ax.set_axisbelow(True)
    ax.axvline(x=values.median(),
               color='blue',
               zorder=2,
               linewidth=2,
               label='Mediana ({0:0.3f})'.format(values.median()),
               linestyle='--')
    ax.axvline(x=values.mean(),
               color='orange',
               zorder=2,
               linewidth=2,
               label='Média ({0:0.3f})'.format(values.mean()),
               linestyle='--')
    ax.set_xlabel('Volume / mL', size=15)
    ax.set_ylabel('Frequência', size=15)

    lines, labels = ax.get_legend_handles_labels()

    if outlier:
        legend_outlier = Line2D(range(1),
                                range(1),
                                color="w",
                                marker='o',
                                markerfacecolor="c",
                                markersize=10,
                                linewidth=0,
                                markeredgecolor="k")
        lines.append(legend_outlier)  # add new patches and labels to list
        labels.append("Boxplot outliers")

    ax.legend(lines,
              labels,
              fontsize=12,
              loc='upper left',
              bbox_to_anchor=(0.75, 1))


def plot_boxplot(values, ax=None):
    """Box plot

    Parameters
    ----------
    values : array
        Sequência de valores. Pode ser uma série de um Pandas DataFrame
    ax : Matplotlib Axes, optional
        Eixos nos quais serão aplicados os parâmetros, by default None
    """
    plot_param(ax)
    flierprops = dict(markerfacecolor='c', marker='o', markersize=10)
    meanlineprops = dict(linestyle='--', linewidth=2, color='orange')
    medianprops = dict(linestyle='--', linewidth=2, color='blue')

    ax.boxplot(values,
               vert=False,
               meanline=True,
               showmeans=True,
               notch=False,
               labels=[''],
               flierprops=flierprops,
               meanprops=meanlineprops,
               medianprops=medianprops,
               widths=0.95,
               patch_artist=True,
               boxprops=dict(facecolor='c', alpha=0.5))

    [s.set_visible(False) for s in ax.spines.values()]
    ax.yaxis.set_visible(False)
