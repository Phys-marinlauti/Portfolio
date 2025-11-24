#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <cmath>
#include <numeric>
#include <algorithm>

using namespace std;

//Definición de constantes
const int NUM_FEATURES = 72; 

/**
 * @brief Carga un vector de doubles desde un archivo de texto.
 */
vector<double> load_vector_from_file(const string& filename) {
    vector<double> data;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: No se pudo abrir el archivo " << filename << endl;
        return data;
    }
    double value;
    while (file >> value) {
        data.push_back(value);
    }
    file.close();
    return data;
}


vector<double> scale_features(const vector<double>& raw_features, 
                              const vector<double>& means, 
                              const vector<double>& stds) {
    if (raw_features.size() != NUM_FEATURES || means.size() != NUM_FEATURES || stds.size() != NUM_FEATURES) {
        cerr << "Error en dimensiones para el escalado." << endl;
        return {};
    }

    vector<double> scaled_features(NUM_FEATURES);
    for (int i = 0; i < NUM_FEATURES; ++i) {
       
        scaled_features[i] = (raw_features[i] - means[i]) / stds[i];
    }
    return scaled_features;
}


double predict_change(const vector<double>& scaled_features, const vector<double>& weights, double intercept) {
    double prediction = intercept;


    for (int i = 0; i < NUM_FEATURES; ++i) {
        prediction += scaled_features[i] * weights[i];
    }
    return prediction;
}

int main() {
    //1) Cargo Parámetros del Modelo
    vector<double> weights_with_intercept = load_vector_from_file("model_weights.txt");
    if (weights_with_intercept.size() != NUM_FEATURES + 1) {
        cerr << "Error: Número incorrecto de pesos." << endl;
        return 1;
    }
    double intercept = weights_with_intercept.back();
    vector<double> weights(weights_with_intercept.begin(), weights_with_intercept.begin() + NUM_FEATURES);

    //2) Cargo Parámetros del Scaler
    vector<double> means = load_vector_from_file("model_means.txt");
    vector<double> stds = load_vector_from_file("model_stds.txt");
    if (means.size() != NUM_FEATURES || stds.size() != NUM_FEATURES) {
        cerr << "Error: Número incorrecto de parámetros de escalado." << endl;
        return 1;
    }

    //3) Cargo la Última Muestra de Features (Simulación de Tiempo Real)
    vector<double> last_raw_features = load_vector_from_file("last_features_raw.txt");
    if (last_raw_features.size() != NUM_FEATURES) {
        cerr << "Error: Número incorrecto de features." << endl;
        return 1;
    }
    
    // El precio actual (P_t) se almacena en el primer feature
    double current_mid_price = last_raw_features[0];


    //4)Ejecución

    vector<double> scaled_features = scale_features(last_raw_features, means, stds);
    if (scaled_features.empty()) return 1;


    double predicted_change = predict_change(scaled_features, weights, intercept);


    double predicted_mid_price = current_mid_price + predicted_change;

  
    cout.precision(4); //4 decimales
    cout << fixed;

    cout << "Resultado de Forecasting de Cortísimo Plazo" << endl;
    cout << "Precio Actual (Mid-Price AL30): " << current_mid_price << endl;
    cout << "Cambio de Precio Predicho (Delta P): " << predicted_change << endl;
    cout << "Mid-Price Predicho (P_t+1): " << predicted_mid_price << endl;
   
    return 0;
}   