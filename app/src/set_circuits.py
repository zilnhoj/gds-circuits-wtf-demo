import pandas as pd
import random
import gspread

from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'app/src/creds/sde_service_account.json',
    scopes=scopes
)

ct_sheet_key = '1AFAUe_AePKh0XZpTiAVn6CjeKSHyMGFbTDBU2j2souA'
ws_name = 'primary_sheet'

gc = gspread.authorize(credentials)
sheet = gc.open_by_key(ct_sheet_key)
sh = sheet.worksheet(ws_name)
df = pd.DataFrame(sh.get_all_records())


set_df = pd.DataFrame()
exercise_type_ls = ['arms', 'legs', 'tums', 'cardio','arms', 'legs', 'tums', 'cardio','arms', 'legs', 'tums', 'cardio',
'arms', 'legs', 'tums', 'cardio','arms', 'tums']
daily_circuit_df = pd.DataFrame()
func_df = pd.DataFrame()

def render_plots():
    return



def get_circuit(date, session):
    cir_session = session
    cir_date = date
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(ct_sheet_key)
    sh = sheet.worksheet(ws_name)
    df = pd.DataFrame(sh.get_all_records())
    exercises_df = __get_exercises_set(df, cir_session)
    sets_dict = __exercise_dict(exercises_df)
    session_df = __get_exercises(df, sets_dict, cir_date, cir_session)
    return session_df

# use the results from get_circuit to feed into a def to show the df as a bokeh chart

def __get_exercises_set(cir_df, cir_session):
    if cir_session=='Ttwelvex40sx2':
        return cir_df.loc[df['40X20'] == 'Y']
    elif cir_session=='6x1x3':
        return cir_df.loc[df['1minX6'] == 'Y']
    else:
        return cir_df.loc[df['reps_12'] == 'Y']

def __exercise_dict(df):
    return {k: g["exercise"].tolist() for k, g in df.groupby("type")}

def __get_exercises(df, sets_dict, cir_date, cir_session):
    print(f'cir_session in get_circuits function {cir_session}')
    sets_dict = __exercise_dict(df)
    daily_circuit_df = pd.DataFrame()
    if cir_session == 'Ttwelvex40sx2':
        for exercise_type in exercise_type_ls[0:12]:
            workout = {k: random.choice(v) for k, v in sets_dict.items()}
            func_df = pd.DataFrame({
                'Circuit': workout[exercise_type],
                'Work': '40',
                'Rest': '20'
            }, index=[0])

            daily_circuit_df = pd.concat([daily_circuit_df, func_df])

        return daily_circuits_df
        # worksheet = sheet.add_worksheet(title=f"{CIRCUITS_DATE}_TWELVE_X_40_W_20_X2", rows=20, cols=4)
        # if worksheet in worksheet_ls:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
        # else:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())

    elif cir_session == '6x1x3':

        for exercise_type in exercise_type_ls:
            workout = {k: random.choice(v) for k, v in sets_dict.items()}
            func_df = pd.DataFrame({
                'Circuit': workout[exercise_type],
                'Work': '1 min',
                'Rest': '2 between sets'
            }, index=[0])

            daily_circuit_df = pd.concat([daily_circuit_df, func_df])
        return daily_circuit_df

        # worksheet = sheet.add_worksheet(title=f"{CIRCUITS_DATE}_ONE_MIN_X_6_X_3", rows=20, cols=4)
        # worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
        # if worksheet in worksheet_ls:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
        # else:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
    else:
        for exercise_type in exercise_type_ls[0:12]:
            workout = {k: random.choice(v) for k, v in sets_dict.items()}
            func_df = pd.DataFrame({
                'Type': exercise_type,
                'Circuit': workout[exercise_type],
                'Work': '12 reps',
                'Rest': '2 mins between sets'
            }, index=[0])

            daily_circuit_df = pd.concat([daily_circuit_df, func_df])
        return daily_circuit_df
        # worksheet = sheet.add_worksheet(title=f"{CIRCUITS_DATE}_twelve_X_6_X_3", rows=20, cols=4)
        # worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
        # if worksheet in worksheet_ls:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())
        # else:
        #     worksheet.update([daily_circuit_df.columns.values.tolist()] + daily_circuit_df.values.tolist())





