from bokeh.plotting import figure, show, output_file
from src.features.build_features import word_count, create_document

def word_count_year(all_years):
    years = []
    word_counts = []

    for year in all_years:
        years.append(year)
        word_counts.append(word_count(create_document(year)))

    p1 = figure(title="Word Count Per Year")
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Year'
    p1.yaxis.axis_label = 'Words'

    p1.line(years, word_counts, color='#A6CEE3')
    show(p1)
    return output_file("line.html")

def main():
    word_count_year(range(1977, 2017))

if __name__ == '__main__':
    main()


