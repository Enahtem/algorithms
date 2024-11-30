import numpy as np
import json

#THis will be a 2d polynomial bayesian regression thing

# Input Data (Likely generated from clicking website or uploading json)
#Example Input (Add prior parameter variance and model variance later)
#Also add input start and input end, solution x num and y num. degree of solution.
jsonRawData = '''
{
    "points": [
        [1.0, 2.0],
        [4.0, 5.0],
        [7.0, 8.0]
    ]
}
'''

rawData = json.loads(jsonRawData)
data = np.array(rawData["points"])

print(data)
# Splitting Data (Train/Validation, Test)

# Bayesian Regression Formula
# Send the calculated solution points back
