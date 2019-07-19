from web_scrap.heroes_process import get_current_hero_trends
from web_scrap.scrap_constant import heroes_trend_image_path
import pandas as pd
from utility import render_mpl_table


def round_df_digits(df):
    df = (df.astype(float).applymap('{:,.2f}'.format))
    return df


def get_current_trend():
    current_trend_dataframe = get_current_hero_trends()
    current_trend_dataframe = current_trend_dataframe[:10]
    alphabetic_df = current_trend_dataframe[current_trend_dataframe.columns[0]]
    numeric_df = current_trend_dataframe[current_trend_dataframe.columns[1:]]
    numeric_df = round_df_digits(numeric_df)
    current_trend_dataframe = pd.concat([alphabetic_df, numeric_df], axis=1)
    # image_path = DataFrame_to_image(current_trend_dataframe, outputfile=heroes_trend_image_path)
    title = 'Current Heroes Trend \nWR: Win Rate, PR: Pick Rate'
    table = render_mpl_table(current_trend_dataframe, header_columns=0, col_width=2.0,
                             title=title)
    # return image_path


if __name__ == '__main__':
    print(get_current_trend())


