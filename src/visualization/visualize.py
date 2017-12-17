from bokeh.plotting import figure, show, output_file
from src.features.build_features import get_word_count, create_document, get_sentence_count, get_brk, get_sp

def word_count_year(all_years):
    years = []
    word_counts = []
    sentence_counts = []

    for year in all_years:
        years.append(year)
        word_counts.append(get_word_count(create_document(year)))
        sentence_counts.append(get_sentence_count(create_document(year)))


    p1 = figure(title="Word Count Per Year")
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Year'
    p1.yaxis.axis_label = 'Words'

    p1.line(years, word_counts, color="red", legend = "word counts")
    show(p1)
    return

def buffett_vs_market(all_years):
    years = [all_years[0] - 1]
    buffett = [1]
    sp = [1]
    for year in range(len(all_years)):
        years.append(all_years[year])
        buffett.append(buffett[year] * (1 + get_brk(all_years[year])))
        sp.append(sp[year]* (1 + get_sp(all_years[year])))

    p2 = figure(title = "Buffett Vs the Market")
    p2.grid.grid_line_alpha = 0.3
    p2.xaxis.axis_label = 'Year'
    p2.yaxis.axis_label = 'Returns'

    p2.line(years, buffett, color="red", legend = "Buffett")
    p2.line(years, sp, color="blue", legend = "Market")
    show(p2)


def main():
    #word_count_year(range(1977, 2017))
    buffett_vs_market(range(1981, 2017))

if __name__ == '__main__':
    main()


