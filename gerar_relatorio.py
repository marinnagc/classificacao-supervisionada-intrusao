# -*- coding: utf-8 -*-
"""Gera o relatorio R2_Grigolli_Farias.pdf a partir dos numeros conferidos no notebook."""
from fpdf import FPDF

PAGE_W = 210
MARGIN = 16
COL_W = PAGE_W - 2 * MARGIN

RED = (172, 22, 40)
RED_DARK = (120, 15, 28)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
GRAY_LIGHT = (243, 243, 243)
GRAY_LINE = (205, 205, 205)

FONT_DIR = "C:/Windows/Fonts/"


class Report(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Sans", "", FONT_DIR + "arial.ttf")
        self.add_font("Sans", "B", FONT_DIR + "arialbd.ttf")
        self.add_font("Sans", "I", FONT_DIR + "ariali.ttf")
        self.add_font("Sans", "BI", FONT_DIR + "arialbi.ttf")
        self.section_no = 0

    def header(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*RED)
        self.set_line_width(0.6)
        self.line(MARGIN, 12, PAGE_W - MARGIN, 12)
        self.set_font("Sans", "", 8)
        self.set_text_color(*GRAY)
        self.set_xy(MARGIN, 8)
        self.cell(0, 5, "Roteiro 2 \u00b7 Classifica\u00e7\u00e3o supervisionada de intrus\u00e3o", align="L")
        self.set_xy(-MARGIN - 60, 8)
        self.cell(60, 5, "Grigolli & Farias", align="R")
        self.set_text_color(*INK)
        self.set_y(18)

    def footer(self):
        self.set_y(-13)
        self.set_font("Sans", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, f"P\u00e1gina {self.page_no()}/6", align="C")
        self.set_text_color(*INK)

    def section_title(self, num, txt):
        self.ln(1)
        self.set_font("Sans", "B", 14)
        self.set_text_color(*RED)
        self.cell(9, 8, f"{num}", align="L")
        self.set_text_color(*INK)
        self.cell(0, 8, txt, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*RED)
        self.set_line_width(0.5)
        y = self.get_y() + 0.5
        self.line(MARGIN, y, PAGE_W - MARGIN, y)
        self.ln(3)

    def sub_title(self, txt):
        self.ln(1)
        self.set_fill_color(*RED)
        y0 = self.get_y()
        self.rect(MARGIN, y0 + 0.5, 1.6, 5.5, style="F")
        self.set_xy(MARGIN + 4, y0)
        self.set_font("Sans", "B", 10.5)
        self.set_text_color(*INK)
        self.cell(0, 6.5, txt, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def body(self, txt, size=9.6):
        self.set_font("Sans", "", size)
        self.set_text_color(*INK)
        self.multi_cell(0, 4.7, txt, align="L")
        self.ln(1)

    def bullet(self, txt, size=9.6):
        self.set_font("Sans", "B", size)
        self.set_text_color(*RED)
        x0, y0 = self.get_x(), self.get_y()
        self.cell(5, 4.7, "\u2022")
        self.set_xy(x0 + 5, y0)
        self.set_font("Sans", "", size)
        self.set_text_color(*INK)
        self.multi_cell(COL_W - 5, 4.7, txt, align="L")
        self.ln(0.8)

    def caption(self, txt, size=8.7):
        self.set_font("Sans", "I", size)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 4.3, txt)
        self.set_text_color(*INK)
        self.ln(0.5)

    def _table_row(self, cells, widths, bold, fill_color, size, line_h, text_color=None):
        self.set_font("Sans", "B" if bold else "", size)
        x0, y0 = self.get_x(), self.get_y()
        n_lines = []
        for val, w in zip(cells, widths):
            lines = self.multi_cell(w - 2, line_h, str(val), border=0, align="C", dry_run=True, output="LINES")
            n_lines.append(max(1, len(lines)))
        row_h = line_h * max(n_lines)
        x = x0
        self.set_fill_color(*fill_color)
        self.set_draw_color(*GRAY_LINE)
        self.set_text_color(*(text_color or INK))
        for val, w, nl in zip(cells, widths, n_lines):
            self.rect(x, y0, w, row_h, style="DF")
            y_text = y0 + (row_h - line_h * nl) / 2
            self.set_xy(x, y_text)
            self.multi_cell(w, line_h, str(val), border=0, align="C")
            x += w
        self.set_text_color(*INK)
        self.set_xy(x0, y0 + row_h)

    def table(self, headers, rows, widths, size=8.3, line_h=4.4, zebra=True):
        self._table_row(headers, widths, True, RED_DARK, size, line_h, text_color=(255, 255, 255))
        for i, row in enumerate(rows):
            fill = GRAY_LIGHT if (zebra and i % 2 == 1) else (255, 255, 255)
            self._table_row(row, widths, False, fill, size, line_h)
        self.ln(2.5)


pdf = Report()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(MARGIN, 16, MARGIN)

# ============================================================ CAPA / PAGINA 1
pdf.add_page()
pdf.set_fill_color(*RED)
pdf.rect(0, 0, PAGE_W, 3, style="F")
pdf.ln(6)
pdf.set_font("Sans", "B", 20)
pdf.set_text_color(*RED)
pdf.cell(0, 10, "Roteiro 2", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Sans", "B", 15)
pdf.set_text_color(*INK)
pdf.cell(0, 8, "Classifica\u00e7\u00e3o supervisionada de intrus\u00e3o", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font("Sans", "", 10.5)
pdf.cell(0, 6, "Dupla: Marinna Grigolli; Vit\u00f3ria Farias", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Sans", "I", 9.5)
pdf.set_text_color(*GRAY)
pdf.cell(0, 6, "C\u00f3digo da dupla: e4817f   \u00b7   random_state: 3833692159   \u00b7   classe dif\u00edcil: Infiltration + Heartbleed",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(*INK)
pdf.set_draw_color(*RED)
pdf.set_line_width(0.5)
pdf.ln(2)
pdf.line(MARGIN, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
pdf.ln(4)

pdf.section_title("1.", "Aquecimento: tabela-s\u00edntese (itens b, c, d)")
pdf.body(
    "Dataset aquecimento_autenticacao.csv (3.160 IPs, 8 sinais, 17,7% de ataque). intervalo_medio_seg fica em "
    "escala de milhares, bem acima das demais colunas (0\u20131 ou 1\u20133); essa diferen\u00e7a de escala "
    "\u00e9 o motivo do experimento do item d)."
)
pdf.body(
    "Regra manual (item b): em vez de copiar o limiar de exemplo do enunciado, olhamos "
    "aquecimento.groupby(\u201clabel\u201d).describe() para achar um corte que realmente separe as classes "
    "nesta base. Nenhum IP benigno tem usuarios_distintos > 3 nem usuarios_inexistentes > 1; nos ataques a "
    "mediana \u00e9 26 e 10, respectivamente. Regra: usuarios_distintos \u2265 4 OU usuarios_inexistentes \u2265 2."
)
pdf.table(
    ["Modelo", "Acur\u00e1cia", "FN", "FP", "Recall ataque"],
    [
        ["Regra manual (item b)", "0,9959", "13", "0", "0,9768"],
        ["\u00c1rvore d=3", "0,9937", "6", "0", "0,9643"],
        ["Reg. log\u00edstica (com scaler)", "0,9831", "16", "0", "0,9048"],
        ["Reg. log\u00edstica (sem scaler)", "0,9947", "3", "2", "0,9821"],
    ],
    [68, 26, 16, 16, 30],
)
pdf.body(
    "A regra manual foi calculada sobre o dataset inteiro (limiar fixo do item b), n\u00e3o s\u00f3 o treino; os "
    "outros tr\u00eas modelos respeitam o split 70/30 estratificado (random_state=3833692159). A regra "
    "recalibrada chega a 99,59%, na verdade melhor que a \u00e1rvore e a regress\u00e3o com scaler. Isso "
    "N\u00c3O significa que a regra seja superior: ela s\u00f3 \u00e9 t\u00e3o boa porque foi calibrada olhando o "
    "describe() do dataset INTEIRO, j\u00e1 sabendo o r\u00f3tulo de cada linha, uma forma de espiar o "
    "problema que n\u00e3o existe em produ\u00e7\u00e3o. A \u00e1rvore e a regress\u00e3o aprendem a fronteira "
    "sozinhas a partir de s\u00f3 70% dos dados (treino) e ainda generalizam bem para o teste: essa \u00e9 a "
    "compara\u00e7\u00e3o que realmente importa."
)

pdf.sub_title("Q1. Features da \u00e1rvore nos 2 primeiros n\u00edveis: coincide com a regra do item b?")
pdf.body(
    "A \u00e1rvore escolhe usuarios_distintos no 1\u00ba n\u00edvel (limiar 3,5) e usuarios_inexistentes no 2\u00ba "
    "(limiar 1,5); falhas s\u00f3 aparece no 3\u00ba n\u00edvel, como crit\u00e9rio residual (limiar 15,5). Isso "
    "concorda muito bem com a regra recalibrada do item b) (limiares 4 e 2 para os mesmos dois sinais, achados "
    "de forma independente: a \u00e1rvore via Gini, a regra via groupby(label).describe()). Bate tamb\u00e9m com "
    "a regress\u00e3o log\u00edstica: usuarios_inexistentes (coef. 6,48) e usuarios_distintos (coef. 6,10) s\u00e3o "
    "os dois coeficientes mais fortes, bem \u00e0 frente de falhas (2,92), tr\u00eas abordagens "
    "independentes concordando nos mesmos dois sinais. A vantagem da \u00e1rvore/regress\u00e3o sobre a regra "
    "manual n\u00e3o est\u00e1 em achar sinais melhores (os tr\u00eas acharam os mesmos), e sim em aprender os "
    "limiares automaticamente a partir S\u00d3 do treino, sem espiar o r\u00f3tulo do dataset inteiro para "
    "calibrar os cortes \u00e0 m\u00e3o como fizemos na regra."
)

pdf.sub_title("Q2. Regress\u00e3o log\u00edstica sem o StandardScaler: acur\u00e1cia e n_iter_. Mecanismo?")
pdf.body(
    "A acur\u00e1cia ficou parecida (at\u00e9 um pouco maior nesse teste espec\u00edfico: 99,47% sem scaler vs. "
    "98,31% com scaler), mas o n\u00famero de itera\u00e7\u00f5es do solver lbfgs saltou de 19 para 759 (quase "
    "40x mais), embora ainda dentro do limite de max_iter=1000 (sem disparar ConvergenceWarning). Mecanismo: "
    "sem padroniza\u00e7\u00e3o, intervalo_medio_seg (escala de milhares) domina numericamente o c\u00e1lculo do "
    "gradiente em rela\u00e7\u00e3o a features como fracao_noturna (escala 0\u20131), deixando a superf\u00edcie "
    "de otimiza\u00e7\u00e3o mal-condicionada; o otimizador precisa de muitos passos pequenos para convergir, e "
    "os coeficientes finais deixam de ter escala compar\u00e1vel entre si (perdem interpretabilidade direta)."
)

pdf.sub_title("Q3. Por que ip_origem n\u00e3o pode ser feature?")
pdf.body(
    "Um endere\u00e7o IP \u00e9 s\u00f3 um identificador: n\u00e3o carrega, por si s\u00f3, nenhum "
    "comportamento generaliz\u00e1vel. Se entrasse no modelo, a \u00e1rvore ou a regress\u00e3o aprenderiam a "
    "decorar \u2018o IP X.X.X.X \u00e9 malicioso\u2019 em vez do padr\u00e3o de comportamento (muitas falhas, "
    "muitos usu\u00e1rios inexistentes etc.). No teste apareceriam IPs nunca vistos no treino, e o modelo "
    "n\u00e3o teria nada a dizer sobre eles: o comportamento aprendido seria memoriza\u00e7\u00e3o, n\u00e3o "
    "generaliza\u00e7\u00e3o, e o modelo ficaria in\u00fatil assim que o atacante trocasse de IP (trivial de "
    "fazer)."
)

# ============================================================ PAGINA 2
pdf.add_page()
pdf.section_title("2.", "CICIDS2017: diagn\u00f3stico e armadilhas encontradas (item e)")
pdf.body(
    "Carregado com encoding=\u2018latin-1\u2019. Shape bruto: 111.679 linhas \u00d7 83 colunas. Defeitos "
    "conhecidos confirmados: 65 colunas com espa\u00e7o no nome, 102 linhas com \u00b1Infinity ou NaN (coluna "
    "Flow Bytes/s), 0 duplicatas exatas (todas as colunas), 8 colunas constantes, 16 colunas id\u00eanticas a "
    "outra."
)
pdf.body(
    "Al\u00e9m dos defeitos conhecidos, o enunciado avisava 3 problemas plantados. Os tr\u00eas foram "
    "encontrados seguindo as dicas do roteiro:"
)
pdf.table(
    ["Armadilha", "Detec\u00e7\u00e3o (c\u00f3digo)", "Impacto (dataset bruto)", "Tratamento"],
    [
        ["1) alertas_ids", "coluna fora do Anexo A +\nm\u00e9dia por classe", "1 coluna, todas as\n111.679 linhas",
         "coluna removida"],
        ["2) vetores id\u00eanticos,\nr\u00f3tulos diferentes", "groupby(todas as features)\n.nunique(r\u00f3tulo) > 1",
         "145 grupos / 304 linhas", "linhas removidas"],
        ["3) quase-duplicatas\nmascaradas por contexto", "duplicated(subset=features+\nr\u00f3tulo) vs. default",
         "5.697 linhas em grupos;\n4.530 \u2018extras\u2019 a remover", "drop_duplicates(subset=\nfeatures+r\u00f3tulo)"],
    ],
    [36, 46, 44, 34],
    size=7.7,
)
pdf.body(
    "Armadilha 1: alertas_ids n\u00e3o pertence a nenhuma fam\u00edlia do CICFlowMeter (Anexo A); sua m\u00e9dia "
    "fica perto de 0 em BENIGN e salta para ~2,0\u20132,9 em qualquer classe de ataque, um sinal "
    "quase-bin\u00e1rio s\u00f3 explic\u00e1vel como vazamento de r\u00f3tulo (a coluna s\u00f3 poderia ter sido "
    "calculada depois de algu\u00e9m j\u00e1 saber que o fluxo era malicioso). Um modelo treinado com ela "
    "chegaria perto de 100% de acur\u00e1cia sem aprender nada sobre a rede, e desabaria em produ\u00e7\u00e3o "
    "(onde esse \u2018alerta\u2019 n\u00e3o existiria antes da pr\u00f3pria classifica\u00e7\u00e3o)."
)
pdf.body(
    "Armadilha 2: o mesmo vetor de features aparece com r\u00f3tulos diferentes (ex.: [BENIGN, DDoS]); "
    "nenhum classificador determin\u00edstico acerta os dois ao mesmo tempo; s\u00e3o exemplos com ru\u00eddo "
    "irredut\u00edvel no r\u00f3tulo (tipicamente fluxos muito curtos/degenerados, com assinatura "
    "estat\u00edstica achatada)."
)
pdf.body(
    "Armadilha 3: drop_duplicates() padr\u00e3o exige que TODAS as colunas sejam iguais, inclusive as de "
    "contexto (dia, turno, ordem_captura), que s\u00e3o metadados de quando a linha foi registrada, n\u00e3o do "
    "fluxo em si. O mesmo fluxo repetido com contexto diferente passa despercebido pelo duplicated() default; "
    "sem remov\u00ea-lo, o split aleat\u00f3rio do item h) vazaria a \u2018mesma\u2019 observa\u00e7\u00e3o entre "
    "treino e teste."
)
pdf.caption(
    "Nota de rigor: ap\u00f3s as etapas anteriores da limpeza (remo\u00e7\u00e3o de Inf/NaN e da coluna "
    "alertas_ids) j\u00e1 terem alterado a popula\u00e7\u00e3o e as colunas de agrupamento, reaplicar as mesmas "
    "checagens DENTRO do pipeline sequencial remove 329 linhas (armadilha 2) e 6.030 linhas (armadilha 3), "
    "n\u00fameros diferentes de 304/4.530 porque medem o efeito da etapa em sequ\u00eancia, n\u00e3o o dataset "
    "bruto original. Ambos os n\u00fameros est\u00e3o registrados no notebook; usamos os do dataset bruto "
    "(304/4.530) no parecer por serem a caracteriza\u00e7\u00e3o direta e reprodut\u00edvel do problema na fonte."
)
pdf.body(
    "Shape final ap\u00f3s toda a limpeza (duplicatas exatas, Inf/NaN, 3 armadilhas, colunas constantes e "
    "colunas duplicadas): 105.218 linhas \u00d7 65 colunas."
)

# ============================================================ PAGINA 3
pdf.add_page()
pdf.section_title("3.", "Separabilidade (item f) e engenharia de features (item g)")
pdf.body(
    "Para cada classe de ataque, buscamos (s\u00f3 no treino) a feature e o limiar de uma \u00e1rvore de "
    "profundidade 1 que atinge recall \u2265 0,9 e precis\u00e3o \u2265 0,5 contra BENIGN:"
)
pdf.table(
    ["Classe", "Melhor feature", "Recall", "Precis\u00e3o", "Limiar", "OK?"],
    [
        ["FTP-Patator", "Destination Port", "1,000", "0,933", "21,5", "sim"],
        ["SSH-Patator", "Destination Port", "1,000", "0,806", "23,0", "sim"],
        ["Heartbleed", "Bwd Pkt Len Max", "1,000", "1,000", "11584", "sim"],
        ["PortScan", "Total Len Fwd Pkts", "0,995", "0,531", "3,0", "sim"],
        ["DoS Hulk", "Bwd Pkt Len Std", "0,852", "0,988", "1545,3", "n\u00e3o"],
        ["DoS Slowhttptest", "Flow IAT Mean", "0,799", "0,711", "1,05e7", "n\u00e3o"],
        ["DoS GoldenEye", "Bwd Pkt Len Std", "0,664", "0,984", "1722,1", "n\u00e3o"],
        ["DDoS", "Bwd Pkt Len Std", "0,619", "0,984", "1489,9", "n\u00e3o"],
        ["DoS slowloris", "Active Std", "0,330", "0,924", "4,52e6", "n\u00e3o"],
        ["Infiltration", "Total Len Fwd Pkts", "0,231", "0,857", "282455", "n\u00e3o"],
        ["Web Attack-Brute Force", "Destination Port", "0,000", "0,000", "80,5", "n\u00e3o"],
        ["Bot", "Destination Port", "0,000", "0,000", "1840,5", "n\u00e3o"],
        ["Web Attack-Sql Inj.", "Destination Port", "0,000", "0,000", "80,5", "n\u00e3o"],
        ["Web Attack-XSS", "Destination Port", "0,000", "0,000", "80,5", "n\u00e3o"],
    ],
    [37, 39, 16, 18, 20, 14],
    size=7.6,
)
pdf.body(
    "Separ\u00e1veis por 1 feature: FTP-Patator, SSH-Patator, Heartbleed, PortScan. Todos t\u00eam "
    "assinatura de rede extrema e fixa (porta de destino constante, resposta gigante no vazamento de "
    "mem\u00f3ria, pacotes de sondagem quase vazios). As demais dependem de combina\u00e7\u00e3o de sinais "
    "(volume + tempo + varia\u00e7\u00e3o de tamanho)."
)
pdf.body(
    "Classe dif\u00edcil (Infiltration + Heartbleed): mesmo com a melhor feature combinada (Bwd Packet Length "
    "Max), recall de apenas 0,235; o histograma mostra a distribui\u00e7\u00e3o quase toda sobreposta a "
    "BENIGN. O motivo \u00e9 estrutural: Heartbleed sozinho \u00e9 quase perfeitamente separ\u00e1vel, mas "
    "Infiltration n\u00e3o tem assinatura de flow-stats nenhuma (imita tr\u00e1fego interno leg\u00edtimo por "
    "design); juntar os dois num s\u00f3 r\u00f3tulo faz qualquer feature que isole um atrapalhar o outro."
)
pdf.sub_title("Engenharia de features (item g): 5 features derivadas, cada uma testada")
pdf.body(
    "fe_bytes_por_pacote, fe_razao_fwd_bwd_bytes, fe_header_payload_ratio, fe_idle_active_ratio, "
    "fe_flag_diversity: nenhuma isola sozinha a classe dif\u00edcil (recall e precis\u00e3o zerados no "
    "teste de limiar \u00fanico), resultado esperado e documentado, j\u00e1 que a classe dif\u00edcil mistura dois "
    "mecanismos opostos de ataque. Ainda assim, 2 delas (fe_header_payload_ratio e fe_bytes_por_pacote) "
    "aparecem no top-15 de import\u00e2ncia do Random Forest (item i), ajudando em combina\u00e7\u00e3o com "
    "outras features, mesmo n\u00e3o resolvendo isoladamente."
)

pdf.sub_title("Q4. Armadilhas encontradas: qual a mais perigosa e por que a acur\u00e1cia seria mentira?")
pdf.body(
    "As 3: alertas_ids (vazamento de r\u00f3tulo), vetores id\u00eanticos com r\u00f3tulos diferentes (304 "
    "linhas), quase-duplicatas mascaradas por contexto (4.530 linhas). A mais perigosa \u00e9 alertas_ids: por "
    "ser derivada do pr\u00f3prio r\u00f3tulo, um modelo treinado com ela chegaria perto de 100% de "
    "acur\u00e1cia. Esse n\u00famero seria mentira porque, em produ\u00e7\u00e3o, esse \u2018alerta\u2019 "
    "n\u00e3o existe antes da pr\u00f3pria classifica\u00e7\u00e3o: o modelo estaria lendo a resposta da "
    "prova, n\u00e3o aprendendo padr\u00f5es de tr\u00e1fego generaliz\u00e1veis."
)

# ============================================================ PAGINA 4
pdf.add_page()
pdf.section_title("4.", "Random Forest: split aleat\u00f3rio \u00d7 temporal (itens h, i, j)")
pdf.table(
    ["Split", "Acur\u00e1cia", "Macro-F1", "Recall Infiltr.", "Recall Heartbl.", "Recall BENIGN"],
    [
        ["Aleat\u00f3rio 70/30", "0,9891", "0,9228", "0,833", "1,000", "0,9985"],
        ["Temporal (campanha)", "0,9388", "0,7973", "0,833", "1,000", "0,9730"],
    ],
    [36, 22, 22, 28, 28, 29],
    size=7.9,
)
pdf.body("Recall por classe, aleat\u00f3rio \u00d7 temporal (ordenado pela maior queda):")
pdf.table(
    ["Classe", "Recall aleat.", "Recall temp.", "Queda"],
    [
        ["Bot", "0,978", "0,155", "0,823"],
        ["Web Attack - Sql Injection", "0,833", "0,143", "0,690"],
        ["DoS slowloris", "0,995", "0,832", "0,163"],
        ["DoS Hulk", "0,996", "0,871", "0,125"],
        ["DoS Slowhttptest", "0,993", "0,868", "0,125"],
        ["Web Attack - XSS", "0,359", "0,313", "0,045"],
        ["Web Attack - Brute Force", "0,790", "0,754", "0,036"],
        ["DoS GoldenEye", "0,992", "0,960", "0,033"],
        ["BENIGN", "0,999", "0,973", "0,026"],
        ["SSH-Patator", "0,995", "0,987", "0,008"],
        ["FTP-Patator", "0,998", "0,993", "0,005"],
        ["DDoS", "0,992", "0,988", "0,004"],
        ["PortScan", "0,989", "0,988", "0,002"],
        ["Heartbleed / Infiltration", "1,000 / 0,833", "1,000 / 0,833", "0,000"],
    ],
    [58, 30, 30, 19],
    size=7.6,
)
pdf.body(
    "feature_importances_ (item i): nenhuma feature domina isoladamente (maior import\u00e2ncia ~0,05, sem "
    "nada acima de 0,3), o que confirma que a limpeza do item e) funcionou. Se alertas_ids ainda "
    "estivesse l\u00e1, dominaria essa lista sozinha. fe_header_payload_ratio e fe_bytes_por_pacote (item g) "
    "aparecem no top-15."
)

pdf.sub_title("Q5. Classes separ\u00e1veis por 1 feature \u00d7 classe dif\u00edcil: diferen\u00e7a em termos de rede")
pdf.body(
    "Separ\u00e1veis: FTP-Patator, SSH-Patator, Heartbleed, PortScan. N\u00e3o separ\u00e1veis: DoS "
    "(Hulk/Slowhttptest/GoldenEye/slowloris), DDoS, Infiltration, Web Attack (Brute Force/Sql "
    "Injection/XSS), Bot. As separ\u00e1veis t\u00eam uma assinatura de protocolo fixa e extrema que nenhum "
    "tr\u00e1fego normal replica (porta constante, pacote de resposta gigante, sondagem quase vazia). A classe "
    "dif\u00edcil mistura um ataque com assinatura fort\u00edssima (Heartbleed) com outro sem assinatura de "
    "flow-stats nenhuma (Infiltration imita tr\u00e1fego interno leg\u00edtimo por design); nenhum corte "
    "\u00fanico resolve o par junto."
)

pdf.sub_title("Q6. Classe que mais caiu no temporal: evid\u00eancia e mudan\u00e7a no comportamento do atacante")
pdf.body(
    "Bot: de recall 0,978 (aleat\u00f3rio) para 0,155 (temporal), queda de 0,823, a maior e mais robusta "
    "(quase 2.000 linhas, concentradas na sexta-feira). Medianas in\u00edcio \u00d7 fim da campanha: Flow "
    "Duration 58.821 \u2192 1.002.738 (17x maior); Fwd Packet Length Mean 42,4 \u2192 0,0 bytes; Flow Bytes/s "
    "131.868 \u2192 17,9; Flow Packets/s 1.046 \u2192 6,0. O atacante muda de um \u2018check-in\u2019 ruidoso e "
    "ativo (curto, com dados de verdade) para \u2018beaconing\u2019 silencioso (conex\u00f5es longas, quase sem "
    "payload), padr\u00e3o cl\u00e1ssico de C2 que o modelo, treinado s\u00f3 no in\u00edcio, nunca "
    "aprendeu a reconhecer."
)

# ============================================================ PAGINA 5
pdf.add_page()
pdf.section_title("5.", "Quest\u00f5es finais e parecer contra a produ\u00e7\u00e3o (item k)")
pdf.sub_title("Q7. O split temporal \u00e9 injusto com o modelo, ou \u00e9 a \u00fanica avalia\u00e7\u00e3o honesta?")
pdf.body(
    "\u00c9 a \u00fanica honesta. Em produ\u00e7\u00e3o o modelo \u00e9 treinado com o hist\u00f3rico "
    "dispon\u00edvel e testado contra tr\u00e1fego futuro nunca visto; o split aleat\u00f3rio embaralha "
    "in\u00edcio e fim da mesma campanha entre treino e teste, deixando o modelo \u2018espiar\u2019 um "
    "peda\u00e7o do padr\u00e3o final durante o treino, o que n\u00e3o existe na vida real, onde o futuro "
    "\u00e9 por defini\u00e7\u00e3o desconhecido no momento do treino. A queda de 98,9% para 93,9% de "
    "acur\u00e1cia (e do recall do Bot, de 0,98 para 0,16) mostra que boa parte do desempenho "
    "\u2018aleat\u00f3rio\u2019 era memoriza\u00e7\u00e3o de um recorte espec\u00edfico da campanha, n\u00e3o "
    "capacidade real de generalizar."
)
pdf.sub_title("Q8. A feature do item j (fe_iat_por_byte) ajudou?")
pdf.body(
    "N\u00e3o ajudou: o recall de Infiltration no split temporal ficou id\u00eantico (0,833, os mesmos 2 "
    "de 12 fluxos errados) antes e depois de acrescentar a feature, que ficou entre a posi\u00e7\u00e3o 26 e 27 "
    "de 67 em import\u00e2ncia (varia \u00b11 posi\u00e7\u00e3o entre execu\u00e7\u00f5es do Random Forest). "
    "Isso revela um limite estrutural: com apenas 38 exemplos de Infiltration em todo o dataset (12 no teste "
    "temporal), engenharia de features n\u00e3o cria informa\u00e7\u00e3o que n\u00e3o est\u00e1 nos dados. "
    "Os 2 fluxos que erram caem numa regi\u00e3o t\u00e3o rara e extrema do espa\u00e7o de features "
    "(fe_iat_por_byte e Flow IAT Mean muito acima at\u00e9 da mediana dos pr\u00f3prios acertos de "
    "Infiltration) que nenhuma raz\u00e3o calculada a partir das mesmas colunas resolve; falta exemplos de "
    "treino cobrindo esse extremo, n\u00e3o falta uma feature melhor."
)

pdf.ln(1)
pdf.set_font("Sans", "B", 11.5)
pdf.set_text_color(*RED)
pdf.cell(0, 7, "Parecer t\u00e9cnico: sobre colocar o modelo em produ\u00e7\u00e3o na segunda-feira",
         new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(*INK)
pdf.body(
    "Recomendo N\u00c3O aprovar o deploy do modelo atual no IDS com base apenas na acur\u00e1cia de split "
    "aleat\u00f3rio. Cinco pontos, cada um ancorado num n\u00famero deste notebook:", size=9.4
)
pdf.bullet(
    "A acur\u00e1cia de 98,9% do split aleat\u00f3rio (item h) n\u00e3o sobrevive ao teste honesto. No split "
    "temporal, que simula produ\u00e7\u00e3o (treinar com o passado, testar no futuro), a "
    "acur\u00e1cia cai para 93,9% e o macro-F1 despenca de 0,923 para 0,797. Parte do desempenho "
    "\u2018aleat\u00f3rio\u2019 \u00e9 memoriza\u00e7\u00e3o, n\u00e3o generaliza\u00e7\u00e3o.",
    size=9.4,
)
pdf.bullet(
    "O recall de Bot desaba de ~0,98 para ~0,16 no split temporal (item h). Em produ\u00e7\u00e3o, um C2 de "
    "botnet que muda de comportamento ao longo da campanha passaria despercebido em ~84% das vezes depois da "
    "fase inicial: o IDS ficaria cego justamente na fase mais longa e discreta do ataque.",
    size=9.4,
)
pdf.bullet(
    "O experimento do item l) (treinar seg-qui, testar sex) mostra o pior cen\u00e1rio poss\u00edvel: ataque "
    "nunca visto antes. Bot foi classificado como BENIGN em 100% dos casos; DDoS foi confundido "
    "majoritariamente com DoS Hulk. Um ataque novo, ou vira tr\u00e1fego normal (o pior erro para um IDS), ou "
    "vira um ataque diferente do que \u00e9 (atrapalha a resposta a incidente).",
    size=9.4,
)
pdf.bullet(
    "O dataset de origem tinha 3 armadilhas que s\u00f3 apareceram investigando, n\u00e3o olhando describe() "
    "(item e). Uma delas (alertas_ids) era vazamento de r\u00f3tulo puro: se n\u00e3o removida, os 98,9% "
    "citados pelo gestor poderiam estar inflados por uma coluna que n\u00e3o existiria em produ\u00e7\u00e3o.",
    size=9.4,
)
pdf.bullet(
    "304 linhas do dataset bruto tinham o mesmo vetor de features com r\u00f3tulos diferentes, e outras 4.530 "
    "eram c\u00f3pias quase-id\u00eanticas do mesmo fluxo mascaradas pelas colunas de contexto (item e). Mesmo "
    "o r\u00f3tulo \u2018verdade\u2019 do CICIDS2017 tem ru\u00eddo: toda m\u00e9trica de acur\u00e1cia "
    "carrega uma margem de erro que a m\u00e9dia de 98% nunca comunica ao gestor.",
    size=9.4,
)
pdf.ln(0.5)
pdf.body(
    "Conclus\u00e3o: o modelo pode ser um bom ponto de partida, mas precisa ser reavaliado com split temporal, "
    "monitorado por classe (n\u00e3o s\u00f3 por acur\u00e1cia agregada) e testado especificamente contra "
    "padr\u00f5es de ataque que mudam de comportamento ao longo do tempo antes de entrar em produ\u00e7\u00e3o.",
    size=9.4,
)

# ============================================================ PAGINA 6
pdf.add_page()
pdf.section_title("6.", "Ataques nunca vistos (item l) e Anexo B")
pdf.body(
    "Random Forest treinado apenas seg-qui (66.687 fluxos), testado na sexta (38.531 fluxos, dia=\u2018sex\u2019). "
    "Bot nunca aparece no treino; DDoS (42), Infiltration (38), PortScan (26) t\u00eam menos de 50 exemplos."
)
pdf.body(
    "Bot (n=1.971): 100% classificado como BENIGN. PortScan (n=8.154): 8.142 viram BENIGN. DDoS (n=8.583): "
    "3.241 viram BENIGN e 5.342 viram DoS Hulk. Um classificador supervisionado s\u00f3 reconhece o que j\u00e1 "
    "viu rotulado no treino: contra um ataque genuinamente novo, ele s\u00f3 absorve na classe majorit\u00e1ria "
    "(BENIGN, o sil\u00eancio mais perigoso) ou empresta o r\u00f3tulo do ataque conhecido mais parecido (DDoS "
    "\u2192 DoS Hulk, que ao menos dispara um alerta, s\u00f3 que errado). N\u00e3o \u00e9 defeito de "
    "implementa\u00e7\u00e3o: \u00e9 limita\u00e7\u00e3o estrutural de classifica\u00e7\u00e3o "
    "supervisionada fechada. Um IDS de produ\u00e7\u00e3o precisa de detec\u00e7\u00e3o de anomalia "
    "complementar e retreino frequente."
)

pdf.ln(2)
pdf.set_fill_color(*RED)
pdf.rect(MARGIN, pdf.get_y(), COL_W, 8, style="F")
pdf.set_font("Sans", "B", 12)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(MARGIN + 3, pdf.get_y() + 1.2)
pdf.cell(0, 6, "Anexo B: Ficha de resultados")
pdf.set_text_color(*INK)
pdf.ln(10)
pdf.set_font("Sans", "", 9.5)
pdf.cell(0, 6, "Dupla: Marinna Grigolli; Vit\u00f3ria Farias        Data: 13/09/2026", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

pdf.sub_title("Aquecimento")
pdf.table(
    ["Modelo", "Acur\u00e1cia", "FN", "FP", "Recall ataque"],
    [
        ["Regra manual (item b)", "0,9959", "13", "0", "0,9768"],
        ["\u00c1rvore d=3", "0,9937", "6", "0", "0,9643"],
        ["Reg. log\u00edstica (com scaler)", "0,9831", "16", "0", "0,9048"],
        ["Reg. log\u00edstica (sem scaler)", "0,9947", "3", "2", "0,9821"],
    ],
    [68, 26, 16, 16, 30],
    size=8,
)
pdf.body(
    "Features do 1\u00ba e 2\u00ba n\u00edvel da \u00e1rvore: usuarios_distintos (1\u00ba, limiar 3,5); "
    "usuarios_inexistentes (2\u00ba, limiar 1,5). Regra manual: usuarios_distintos \u2265 4 OU "
    "usuarios_inexistentes \u2265 2 (limiares achados via groupby(label).describe(), n\u00e3o copiados do "
    "enunciado).",
    size=9,
)

pdf.sub_title("CICIDS2017")
pdf.body(
    "C\u00f3digo da dupla: e4817f     random_state: 3833692159     classe dif\u00edcil: Infiltration + "
    "Heartbleed",
    size=9,
)
pdf.table(
    ["Armadilha / passo de limpeza", "Linhas (ou colunas) afetadas"],
    [
        ["Inf / NaN", "102 linhas"],
        ["Duplicatas exatas", "0"],
        ["Armadilha 1: alertas_ids", "1 coluna (111.679 linhas)"],
        ["Armadilha 2: vetores contradit\u00f3rios", "304 linhas / 145 grupos"],
        ["Armadilha 3: quase-duplicatas mascaradas", "4.530 linhas"],
        ["Total final (linhas \u00d7 colunas)", "105.218 \u00d7 65"],
    ],
    [100, 55],
    size=8,
)
pdf.table(
    ["", "Acur\u00e1cia", "Macro-F1", "Recall classe dif\u00edcil", "Recall BENIGN"],
    [
        ["Split aleat\u00f3rio", "0,9891", "0,9228", "0,833 (Inf.) / 1,000 (Heart.)", "0,9985"],
        ["Split temporal", "0,9388", "0,7973", "0,833 (Inf.) / 1,000 (Heart.)", "0,9730"],
    ],
    [30, 22, 22, 55, 26],
    size=7.6,
)
pdf.body("Classes separ\u00e1veis por uma feature: FTP-Patator, SSH-Patator, Heartbleed, PortScan.", size=9)
pdf.body("Classe que mais caiu no temporal: Bot, de 0,978 para 0,155.", size=9)
pdf.body(
    "Feature do item j: fe_iat_por_byte. Efeito no recall temporal (Infiltration): 0,833 \u2192 0,833 "
    "(sem efeito).",
    size=9,
)

pdf.output("R2_Grigolli_Farias.pdf")
print("PDF gerado. Paginas:", pdf.page_no())
