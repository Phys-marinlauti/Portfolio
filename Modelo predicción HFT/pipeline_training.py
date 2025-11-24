# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from collections import deque


FOLDER = r"AGREGAR ACÁ RUTA PARA LOS CSV'S A IMPORTAR" #CAMBIAR RUTA PARA EJECUTAR




#Creo la función que me permite procesar los 3 instrumentos
def process_instrument(df_raw, suffix) -> pd.DataFrame:
    df_raw['fecha_dt'] = pd.to_datetime(df_raw['fecha_nano'], unit='ns', utc=True)
    df_raw['fecha_dt'] = df_raw['fecha_dt'].dt.tz_convert('America/Argentina/Buenos_Aires')
    df_raw.set_index('fecha_dt', inplace=True)
    df = df_raw.between_time('11:00', '17:00')
    df.reset_index(drop=True, inplace=True)

    if df.empty:
        return pd.DataFrame()

    # Mejor bid
    df_bids = df[(df['side']=='BI') & (df['price']>0)] 
    idx_best_bids = df_bids.groupby('fecha_nano')['price'].idxmax()
    best_bids = df_bids.loc[idx_best_bids][['fecha_nano','price','quantity']].rename(columns={'price':'best_bid_price','quantity':'best_bid_qty'})

    # Mejor ask, mismo proceso que mejor bid
    df_off = df[(df['side']=='OF') & (df['price']>0)]
    idx_best_off = df_off.groupby('fecha_nano')['price'].idxmin()
    best_off = df_off.loc[idx_best_off][['fecha_nano','price','quantity']].rename(columns={'price':'best_offer_price','quantity':'best_offer_qty'})

    #Hago Merge de ToB
    df_tob = pd.merge(best_bids, best_off, on='fecha_nano', how='outer').sort_values('fecha_nano').ffill()



    bid_p = df_tob['best_bid_price']
    ask_p = df_tob['best_offer_price']
    bid_q = df_tob['best_bid_qty']
    ask_q = df_tob['best_offer_qty']

    denom = (bid_q + ask_q).replace(0, np.nan)

#creo las features mid, spread, imbalance, y pressure

    df_tob[f'mid{suffix}'] = (bid_p + ask_p) / 2
    df_tob[f'spread{suffix}'] = ask_p - bid_p
    df_tob[f'imbalance{suffix}'] = (bid_q - ask_q) / denom
    df_tob[f'pressure{suffix}'] = (bid_p*ask_q + ask_p*bid_q) / denom

    df_tob = df_tob[['fecha_nano',
                     f'mid{suffix}',
                     f'spread{suffix}',
                     f'imbalance{suffix}',
                     f'pressure{suffix}']].copy()
    df_tob.dropna(inplace=True)
    return df_tob



LAGS = 5 #cantidad de ticks para mis features lag
NUM_BASE_FEATURES = 12 #cantidad de features independientes
TOTAL_FEATURES_ESPERADOS = NUM_BASE_FEATURES * (1 + LAGS)


#Cargo los csv's
df_ars_raw = pd.read_csv(FOLDER + 'AL30_1205_CI_PESOS.csv')
df_mep_raw = pd.read_csv(FOLDER + 'AL30_1205_CI_MEP.csv')
df_ccl_raw = pd.read_csv(FOLDER + 'AL30_1205_CI_CCL.csv')

#Proceso los 3 csv's
df_ars = process_instrument(df_ars_raw, '_AL30')
df_mep = process_instrument(df_mep_raw, '_AL30D')
df_ccl = process_instrument(df_ccl_raw, '_AL30C')

#Hago merge de los dfs ya procesados
df_tmp = pd.merge_asof(df_ars, df_mep, on='fecha_nano', direction='backward')
df_final = pd.merge_asof(df_tmp, df_ccl, on='fecha_nano', direction='backward')
df_final.dropna(inplace=True)

#Armo la variable target: cambio en el midprice de AL30
df_final['target_change_AL30'] = df_final['mid_AL30'].shift(-1) - df_final['mid_AL30']

#Pesifico las features a partir del tc implícito
df_final['tc_mep'] = df_final['mid_AL30'] / df_final['mid_AL30D']
df_final['tc_ccl'] = df_final['mid_AL30'] / df_final['mid_AL30C']
df_final['spread_AL30D_pesos']    = df_final['spread_AL30D']    * df_final['tc_mep']
df_final['pressure_AL30D_pesos'] = df_final['pressure_AL30D'] * df_final['tc_mep']
df_final['spread_AL30C_pesos']    = df_final['spread_AL30C']    * df_final['tc_ccl']
df_final['pressure_AL30C_pesos'] = df_final['pressure_AL30C'] * df_final['tc_ccl']
df_final = df_final.replace([np.inf,-np.inf], np.nan).ffill().dropna()

base_features = [
    'mid_AL30','spread_AL30','imbalance_AL30','pressure_AL30',
    'tc_mep','spread_AL30D_pesos','imbalance_AL30D','pressure_AL30D_pesos',
    'tc_ccl','spread_AL30C_pesos','imbalance_AL30C','pressure_AL30C_pesos'
]

target_name = 'target_change_AL30'

#Creo las features lag
df_lag = df_final.copy()
all_features = base_features.copy()
for col in base_features:
    for k in range(1,LAGS+1):
        lag_col_name = f"{col}_lag{k}"
        df_lag[lag_col_name] = df_lag[col].shift(k)
        all_features.append(lag_col_name)

df_lag["target"] = df_lag[target_name]
df_lag.dropna(inplace=True)

#Separo mis datos en train y test
split = int(len(df_lag)*0.7)
df_train = df_lag.iloc[:split]
df_test  = df_lag.iloc[split:]

X_train_data = df_train[all_features].values
X_test_data = df_test[all_features].values
y_train = df_train["target"].values
y_test  = df_test["target"].values

scaler = StandardScaler()
scaler.fit(X_train_data)
X_train = scaler.transform(X_train_data)
X_test  = scaler.transform(X_test_data)

#Inicializo el modelo
model = LinearRegression()
model.fit(X_train, y_train)

#Predicciones
preds = model.predict(X_test)
#Calculo el RMSE
rmse = np.sqrt(((preds - y_test)**2).mean())



#Evaluación del modelo

print("\nRMSE TEST (Batch):", rmse) 

print("\n--- Simulación de Predicción BATCH (Primeras 10 filas del Test Set) ---")
df_predicciones = pd.DataFrame({
    'precio_actual': df_test['mid_AL30'],
    'cambio_REAL': y_test,
    'cambio_PREDICHO_batch': preds
})
df_predicciones['precio_PREDICHO_batch'] = df_predicciones['precio_actual'] + df_predicciones['cambio_PREDICHO_batch']
with pd.option_context('display.float_format', '{:,.2f}'.format):
    print(df_predicciones[['precio_actual', 'cambio_REAL', 'cambio_PREDICHO_batch', 'precio_PREDICHO_batch']].head(10))

# Sanity check
print("Resumen de tests a forma de \"Sanity check\"")

errores = []  #Acumulo errores sin cortar ejecución

#1)Reviso RMSE (tomé una cota superior arbitraria de 30 solo como ejemplo)
print(f"RMSE es {rmse:.4f}")
if rmse <= 1e-6:
    errores.append("RMSE es 0. Revisar si hay data leakage.")
if rmse >= 30:
    errores.append("RMSE muy alto.")
if 1e-6 < rmse < 30:
    print("El modelo predice. RMSE entre 0 y 30.")

#2)Dimensiones para C++
print("Chequeo dimensiones para el código de C++")
if len(all_features) != TOTAL_FEATURES_ESPERADOS:
    errores.append(
        f"FALLO: El modelo usa {len(all_features)} features, C++ espera {TOTAL_FEATURES_ESPERADOS}."
    )
if len(model.coef_) != TOTAL_FEATURES_ESPERADOS:
    errores.append(
        f"FALLO: El modelo tiene {len(model.coef_)} pesos, C++ espera {TOTAL_FEATURES_ESPERADOS}."
    )
if len(scaler.mean_) != TOTAL_FEATURES_ESPERADOS:
    errores.append(
        f"FALLO: El scaler tiene {len(scaler.mean_)} medias, C++ espera {TOTAL_FEATURES_ESPERADOS}."
    )
if len(errores) == 0:
    print("Todas las dimensiones (72 features) son correctas.")

#3)Directional Accuracy con umbral fijo (arbitrario)

#Defino un threshhold arbitrario que me sirve como filtro de ruido
THRESH = 0.1 

def to_dir(x, th):
    return np.where(x > th, 1,
           np.where(x < -th, -1, 0))

real_dir = to_dir(y_test, THRESH)
pred_dir = to_dir(preds, THRESH)

directional_accuracy = (real_dir == pred_dir).mean()

print(f"Directional Accuracy (threshold={THRESH}): {directional_accuracy:.4f}")

if directional_accuracy <= 0.33:
    errores.append("El modelo no supera aleatoriedad pura.")

#4) MAE del cambio (MAE_Δ)
print("\nTest 4: MAE del cambio (MAE_Δ)")

mae_change = np.mean(np.abs(preds - y_test))
print(f"MAE_Δ: {mae_change:.4f}")

if mae_change <= 0:
    errores.append("MAE_Δ no puede ser 0.")
if mae_change >= 20:
    errores.append("MAE_Δ demasiado alto; revisar estabilidad del modelo.")
if 0 < mae_change < 20:
    print("MAE del cambio dentro de parámetros razonables.")

# Reporte final sin cortar ejecución
print("\nResumen final:")
if len(errores) == 0:
    True
else:
    for e in errores:
        print(" - " + e)


#Exporto el modelo para implementar C++

#1) Exporto pesos

weights = np.concatenate([model.coef_, [model.intercept_]])
np.savetxt("model_weights.txt", weights)


#2)Exporto mean y std

means = scaler.mean_
stds  = np.maximum(scaler.scale_, 1e-12)  #evito división por cero

np.savetxt("model_means.txt", means)
np.savetxt("model_stds.txt", stds)


#3)Exporto última fila de features


last_raw = df_test[all_features].iloc[-1].values
last_scaled = scaler.transform(last_raw.reshape(1, -1)).flatten()

np.savetxt("last_features_raw.txt", last_raw)
np.savetxt("last_features_scaled.txt", last_scaled) 

#4) Exportar dataset final

df_export = df_test[all_features].copy()
df_export['target'] = y_test
df_export.to_csv("features_final.csv", index=False)
