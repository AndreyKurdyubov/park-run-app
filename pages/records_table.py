import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit import session_state as ss
from utils import menu, authentication, tags_table, link_to_tag, add_control, find_db_files, convert_date_string

# Установка конфигурации страницы
st.set_page_config(layout='wide')

menu()
authenticator, name, authentication_status, username = authentication()

db_name = find_db_files()
if db_name:
    db_name = 'sqlite:///' + db_name[-1]
    st.success(f'Найдена БД от {convert_date_string(db_name[10:-3])}')
    engine = create_engine(db_name)
else:
    st.write('База отсутствует')

def main():
    # таблица тегов
    if username in ['host', 'org']:
        df_tag, _ = tags_table()

    def title(string):
        return string.title()

    def add_button(run_number, list_name, df, i):
        if len(df) != 0:
            df_comb = df.merge(df_tag[['profile_link', 'VK link', "Имя"]], on='profile_link', how='left')
            df_comb['tag'] = df_comb.apply(lambda row: link_to_tag(row['VK link'], row['name'], row['Имя']), axis=1)
            names = df_comb['tag'].values
            profiles = df_comb['profile_link'].values
            positions = df['position'].values
        else:
            names = df['name'].values
            profiles = df['profile_link'].values
            positions = df['position'].values
        add_control(run_number, list_name, names, positions, i)
        return [list_name, len(set(profiles))]

    # Заголовок
    # get last run number and date
    querie = """
    SELECT distinct(CAST(run_number as INT)) as run_number, substr(run_date, 1, 10) as run_date
    FROM runners
    ORDER BY run_number DESC
    LIMIT 5
    """
    df = pd.read_sql(querie, con=engine)
    df["run"] = '#' + df['run_number'].astype(str) + ', ' + df['run_date']

    st.title('Рекорды, новички, клубы 10/25/50/100')
    run_select = st.selectbox("Выбрать номер забега", df["run"])
    run_number = int(run_select.split(",")[0].replace("#", "")) # извлечь только номер забега

    # st.header(run_select)
    ##############################################################################
    tables_summary = []

    # runners
    querie = f'''
    SELECT profile_link, name, 
        substr(run_date, 1, 10) as run_date, 
        CAST(run_number as INT) as run_number, 
        CAST(position as INT) as position, 
        time,
        finishes,
        achievements
    FROM runners
    WHERE CAST(run_number as INT) <= {run_number}
    '''
    df_run = pd.read_sql(querie, con=engine) # all runs for run <= run_number
    df_run_num = df_run[df_run['run_number']==run_number] # only runs for run == run_number

    # orgs
    querie = f'''
    SELECT profile_link, name, 
        substr(run_date, 1, 10) as run_date,
        CAST(run_number as INT) as run_number, 
        GROUP_CONCAT(volunteer_role, ', ') as roles,
        volunteers
    FROM organizers 
    WHERE CAST(run_number as INT) <= {run_number}
    GROUP BY profile_link, run_date
    '''
    df_org = pd.read_sql(querie, con=engine) # all vols for run <= run_number
    df_org_num = df_org[df_org['run_number']==run_number] # only vols for run == run_number

    # # users
    # querie = f'''
    # SELECT profile_link, 
    #     CAST(us.finishes AS INT) as num_fins, 
    #     CAST(us.volunteers AS INT) as num_vols,
    #     peterhof_finishes_count,
    #     peterhof_volunteers_count
    # FROM users us
    # '''
    # df_users = pd.read_sql(querie, con=engine)

    #########################################################################
    list_name = f'Рекорды'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_run_num.query(f'achievements.str.contains("Личный рекорд!")')

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'position', 'time'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'time': st.column_config.Column(label="Рекорд", width=''), 
            'position': st.column_config.Column(label="Позиция", width=''), 
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    # ##############################################
    list_name = f'Первый финиш на 5 верст'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_run_num.query(f'achievements.str.contains("Первый финиш на 5 вёрст")')

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'position', 'time'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'time': st.column_config.Column(label="Время", width=''),
            'position': st.column_config.Column(label="Позиция", width=''), 
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = i + 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    ##############################################
    list_name = f'Первый финиш в Петергофе'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_run_num.query(f'achievements.str.contains("Первый финиш на Петергоф")')

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'position', 'time', 'finishes'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'time': st.column_config.Column(label="Время", width=''),
            'position': st.column_config.Column(label="Позиция", width=''), 
            'finishes': st.column_config.Column(label="# финишей", width='medium'),
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = i + 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    # ##############################################
    list_name = f'Первое волонтерство на 5 верст'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_org_num.merge(df_run_num, how='left', on=['profile_link', 'name', 'run_number', 'run_date'])
    df = df.query('volunteers == "1 волонтёрство"')

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'position', 'time', 'roles'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'time': st.column_config.Column(label="Время", width=''),
            'position': st.column_config.Column(label="Позиция", width=''),
            'roles': st.column_config.Column(label="Роли", width='medium'),
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = i + 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    ##############################################
    # list_name = f'Первое волонтерство в Петергофе'
    # st.header(list_name + f'\n\n**{run_select}**')

    # df = df_org_num.merge(df_users, how='inner', on='profile_link'
    #                       ).merge(df_run_num, how='left', on=['profile_link', 'name', 'run_number', 'run_date'])
    # df = df.query('peterhof_volunteers_count == 1 & volunteers != "1 волонтёрство"')

    # # Отображаем таблицу
    # st.data_editor(
    #     df,
    #     column_order=['profile_link', 'name', 'volunteers', 'position', 'time', 'roles'],
    #     column_config={
    #         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
    #         'name': st.column_config.Column(label="Участник", width='medium'), 
    #         'volunteers': st.column_config.Column(label="# волонтерств", width=''),
    #         'time': st.column_config.Column(label="Время", width=''),
    #         'position': st.column_config.Column(label="Позиция", width=''),
    #         'roles': st.column_config.Column(label="Роли", width='medium'),
    #     },
    #     hide_index=True
    # )

    # if username in ['host', 'org']:
    #     i = i + 1 # button key
    #     new_list = add_button(run_number, list_name, df, i)
    #     tables_summary.append(new_list)

    # ##############################################
    list_name = f'Вступившие в клубы пробегов'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_run_num.query('finishes.str.contains("^10\s|^25\s|^50\s|^100\s|^150\s", regex=True)')

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'finishes', 'position', 'time'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'time': st.column_config.Column(label="Время", width=''),
            'position': st.column_config.Column(label="Позиция", width=''),
            'finishes': st.column_config.Column(label="# финишей", width=''),
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = i + 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    ##############################################
    list_name = f'Вступившие в клубы волонтёрств'
    st.header(list_name + f'\n\n**{run_select}**')

    df = df_org_num.merge(df_run_num, how='left', on=['profile_link', 'name'])
    df = df.query(('volunteers.str.contains("^10\s|^25\s|^50\s|^100\s|^150\s", regex=True)'))

    # Отображаем таблицу
    st.data_editor(
        df,
        column_order=['profile_link', 'name', 'volunteers', 'position', 'time'],
        column_config={
            'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
            'name': st.column_config.Column(label="Участник", width='medium'), 
            'volunteers': st.column_config.Column(label="# волонтерств", width=''),
            'time': st.column_config.Column(label="Время", width=''),
            'position': st.column_config.Column(label="Позиция", width=''),
        },
        hide_index=True
    )

    if username in ['host', 'org']:
        i = i + 1 # button key
        new_list = add_button(run_number, list_name, df, i)
        tables_summary.append(new_list)

    # ##############################################
    # list_name = f'Вторая суббота в Петергофе'
    # st.header(list_name + f'\n\n**{run_select}**')

    # # merging
    # df = df_run.merge(df_org, how='outer', on=['profile_link', 'name', 'run_number', 'run_date']
    #                   ).merge(df_users, on='profile_link').sort_values(by='position', ascending=True)

    # # df['dtype'] = df['roles'].isnull()
    # df['num_subbot'] = df.groupby('profile_link')['run_date'].transform('count')
    # df['first_date'] = df.groupby('profile_link')['run_date'].transform('min')
    # df = df.query(f'run_number == {run_number} & num_subbot == 2')

    # # Отображаем таблицу
    # st.data_editor(
    #     df,
    #     column_order=['profile_link', 'name', 'position', 'roles', 'first_date', 'finishes', 'volunteers'],
    #     column_config={
    #         'profile_link': st.column_config.LinkColumn(label="id 5Вёрст", display_text=r"([0-9]*)$", width=''),
    #         'name': st.column_config.Column(label="Участник", width='medium'), 
    #         'roles': st.column_config.Column(label="Роли", width='medium'),
    #         'position': st.column_config.Column(label="Позиция", width=''),
    #         'time': st.column_config.Column(label="Время", width=''),
    #         'first_date': st.column_config.Column(label="Первая суббота", width=''),
    #         'finishes': st.column_config.Column(label="Количество финишей", width=''),
    #         'volunteers': st.column_config.Column(label="Количество волонтерств", width=''),
    #         'peterhof_finishes_count': st.column_config.Column(label="# финишей в Петергофе", width=''),
    #         'peterhof_volunteers_count': st.column_config.Column(label="# волонтерств в Петергофе", width=''),
    #     },
    #     hide_index=True
    # )

    # if username in ['host', 'org']:
    #     i = i + 1 # button key
    #     new_list = add_button(run_number, list_name, df, i)
    #     tables_summary.append(new_list)

    # #######################################################################
    list_name = 'Протокол'
    # st.header(f"{list_name}\n\n**{run_select}**")

    df_results = df_run_num.merge(df_org_num, how='outer', on=['profile_link', 'name', 'run_number', 'run_date']
                      ).sort_values(by='position', ascending=True)

    if username in ['host', 'org']:
        # i = i + 1 # button key
        # new_list = add_button(run_number, list_name, df_results, i)
        # tables_summary.append(new_list)

        summary = f'''Количество финишеров: {df_results['position'].max():.0f}<br>
                      Количество волонтеров: {len(df_org_num)}<br>
                      Количество уникальных участников: {len(df_results)}<br>
                      Количество неизвестных: {len(df_results.query('not profile_link.str.contains("userstats")'))}<br>
                      '''
        for record in tables_summary:
            summary += f"{record[0]}: {record[1]}<br>"

        st.header("Сводка" + f'\n\n**{run_select}**')
        st.write(summary, unsafe_allow_html=True)

if db_name:
    main()