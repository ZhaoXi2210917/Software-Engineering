import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os

# 1. 加载数据
data = pd.read_csv('data\Fish.csv')

# 2. 数据预处理
X = data[['Species', 'Length1(cm)', 'Length2(cm)']]
y = data['Length3(cm)']

# 3. 特征编码
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(X[['Species']])

# 给 OneHotEncoder 的输出添加列名
encoded_columns = encoder.get_feature_names_out(['Species'])
X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)

# 合并特征并确保列名为字符串类型
X_numeric = pd.concat([X_encoded_df, X[['Length1(cm)', 'Length2(cm)']].reset_index(drop=True)], axis=1)
X_numeric.columns = X_numeric.columns.astype(str)  # 确保所有列名为字符串类型

# 4. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X_numeric, y, test_size=0.2, random_state=42)

# 5. 训练模型
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 6. 测试模型
y_pred = model.predict(X_test)
print(f'Mean Squared Error: {mean_squared_error(y_test, y_pred)}')

# 7. 保存模型和编码器
joblib.dump(model, 'app/Kimi/fish_model.pkl')
joblib.dump(encoder, 'app/Kimi/fish_encoder.pkl')

# 8. 加载模型并预测
def predict_species_length(species, length1, length2):
    model_path = os.path.join(os.path.dirname(__file__), 'fish_model.pkl')
    model = joblib.load(model_path)

    encoder_path = os.path.join(os.path.dirname(__file__), 'fish_encoder.pkl')
    encoder = joblib.load(encoder_path)
    species_encoded = encoder.transform([[species]])
    input_data = pd.concat([pd.DataFrame(species_encoded), pd.DataFrame([[length1, length2]])], axis=1)
    prediction = model.predict(input_data)
    return prediction[0]

if __name__ == "__main__":
    # 示例预测
    species = 'Bream'
    length1 = 25.0
    length2 = 30.0
    prediction = predict_species_length(species, length1, length2)
    print(f'Predicted Length3 for {species} with Length1={length1} and Length2={length2}: {prediction}')
