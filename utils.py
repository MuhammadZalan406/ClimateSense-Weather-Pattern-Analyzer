# utils.py
import numpy as np
import pandas as pd
from scipy import stats

class WeatherAnalyzer:
    def __init__(self, years=10, seed=42):
        self.years = years
        self.months = 12
        np.random.seed(seed)
        self.generate_data()
    
    def generate_data(self):
        """Simulate temperature & rainfall data"""
        # Temperature ~ Normal Distribution
        self.temp_mean = 25
        self.temp_std = 5
        self.temperature = np.random.normal(self.temp_mean, self.temp_std, 
                                           (self.years, self.months))
        
        # Rainfall ~ Binomial Distribution
        self.rain_n = 10
        self.rain_p = 0.4
        self.rainfall = np.random.binomial(self.rain_n, self.rain_p, 
                                          (self.years, self.months)) * 10
        
        # Reshape to 3D: (years, months, features)
        self.data_3d = np.stack([self.temperature, self.rainfall], axis=2)
        
        # Month names
        self.months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    def get_seasonal_patterns(self):
        """Monthly averages over all years"""
        temp_avg = self.temperature.mean(axis=0)
        rain_avg = self.rainfall.mean(axis=0)
        return temp_avg, rain_avg
    
    def detect_anomalies(self, threshold=2):
        """Find anomalies using ±2 std deviation"""
        global_mean = self.temperature.mean()
        global_std = self.temperature.std()
        
        anomalies = np.abs(self.temperature - global_mean) > (threshold * global_std)
        anomaly_indices = np.where(anomalies)
        
        anomaly_list = []
        for y, m in zip(anomaly_indices[0], anomaly_indices[1]):
            anomaly_list.append({
                'year': y + 1,
                'month': self.months_names[m],
                'temperature': round(self.temperature[y, m], 2),
                'mean': round(global_mean, 2),
                'std': round(global_std, 2)
            })
        return anomaly_list
    
    def get_percentile_rank(self):
        """Calculate percentile for each month"""
        all_temps = self.temperature.flatten()
        percentile_rank = np.zeros((self.years, self.months))
        
        for i in range(self.years):
            for j in range(self.months):
                percentile_rank[i, j] = np.sum(all_temps < self.temperature[i, j]) / len(all_temps) * 100
        
        return percentile_rank
    
    def get_extremes(self):
        """Find hottest, coldest, wettest, driest"""
        # Temperature extremes
        hot_idx = np.unravel_index(np.argmax(self.temperature), self.temperature.shape)
        cold_idx = np.unravel_index(np.argmin(self.temperature), self.temperature.shape)
        
        # Rainfall extremes
        wet_idx = np.unravel_index(np.argmax(self.rainfall), self.rainfall.shape)
        dry_idx = np.unravel_index(np.argmin(self.rainfall), self.rainfall.shape)
        
        return {
            'hottest': {'year': hot_idx[0]+1, 'month': self.months_names[hot_idx[1]], 
                       'value': round(self.temperature[hot_idx], 2)},
            'coldest': {'year': cold_idx[0]+1, 'month': self.months_names[cold_idx[1]], 
                       'value': round(self.temperature[cold_idx], 2)},
            'wettest': {'year': wet_idx[0]+1, 'month': self.months_names[wet_idx[1]], 
                       'value': round(self.rainfall[wet_idx], 2)},
            'driest': {'year': dry_idx[0]+1, 'month': self.months_names[dry_idx[1]], 
                      'value': round(self.rainfall[dry_idx], 2)}
        }
    
    def get_statistics(self):
        """Basic statistics for report"""
        return {
            'temp_mean': round(self.temperature.mean(), 2),
            'temp_std': round(self.temperature.std(), 2),
            'temp_min': round(self.temperature.min(), 2),
            'temp_max': round(self.temperature.max(), 2),
            'rain_mean': round(self.rainfall.mean(), 2),
            'rain_std': round(self.rainfall.std(), 2),
            'rain_min': round(self.rainfall.min(), 2),
            'rain_max': round(self.rainfall.max(), 2)
        }
    
    def get_dataframe(self):
        """Convert data to pandas DataFrame for display"""
        df_list = []
        for y in range(self.years):
            for m in range(self.months):
                df_list.append({
                    'Year': y + 1,
                    'Month': self.months_names[m],
                    'Temperature (°C)': round(self.temperature[y, m], 2),
                    'Rainfall (mm)': round(self.rainfall[y, m], 2)
                })
        return pd.DataFrame(df_list)