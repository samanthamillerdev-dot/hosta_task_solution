# Hosta.ai Interview-Task-Solution  


### 1. Challenge
As per requirement `unique_id` in json files were not matching `Object_ID` in csv. Because `unique_id` is in `uuid` format while `Object_ID` in csv is `long-number`. 


### 2. Solution
I got took `item_id` from the image and compared it to `ImageX_Object_ID` fields and when it finds `item_id` in any of the images then it assigns `Host_ID` as its `parent_id` to that image.


### 3. Run script locally

- Make sure you have python installed on your system
- Make sure you have pandas installed on your system
    - If panda is not installed on your system then install it using below command
    - `pip install pandas`

- Run script using below command
    - `python insert_parent_id_into_json.py`