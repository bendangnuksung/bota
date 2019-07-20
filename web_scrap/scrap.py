from web_scrap.heroes_process import get_current_hero_trends
import pandas as pd
from utility import render_mpl_table, get_icon_path, is_file_old
from constant import CT_IMAGE_PATH, CT_IMAGE_UPDATE_TIME_THRESHOLD


def round_df_digits(df):
    df = (df.astype(float).applymap('{:,.2f}'.format))
    return df


def get_current_trend():
    if not is_file_old(CT_IMAGE_PATH, CT_IMAGE_UPDATE_TIME_THRESHOLD):
        return CT_IMAGE_PATH

    current_trend_dataframe = get_current_hero_trends()
    current_trend_dataframe = current_trend_dataframe[:10]
    hero_name_df = current_trend_dataframe[current_trend_dataframe.columns[0]]
    numeric_df = current_trend_dataframe[current_trend_dataframe.columns[1:]]
    numeric_df = round_df_digits(numeric_df)
    heroes_list = hero_name_df.values.tolist()
    icon_path_list = get_icon_path(heroes_list)
    current_trend_dataframe = pd.concat([hero_name_df, numeric_df], axis=1)

    title = 'Current Heroes Trend \n\nWR: Win Rate                              PR: Pick Rate'
    image_path = render_mpl_table(current_trend_dataframe, icon_list=icon_path_list, header_columns=0, col_width=2.6,
                             title=title, font_size=20)
    return image_path


def get_counter_hero(hero):
    pass


if __name__ == '__main__':
    print(get_current_trend())


