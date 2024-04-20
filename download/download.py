# take 19 mins with limited api
# output data already saved in data/od_metro2metro_result.csv and data/od_metro2cbd_result.csv
def get_js(keys,df,num,out_file):
    origin = df.iloc[num,2][0]
    destination = df.iloc[num,2][1]
    name = df.iloc[num,1]
    key = np.random.choice(keys)
    url = f'https://restapi.amap.com/v3/direction/transit/integrated?origin={origin}&destination={destination}&city=023&output=json&key={key}&strategy=0'
    print(url)
    
    dt = requests.get(url).json()
    
    dic = {}
    if dt['info']=='OK':
        if len(dt['route']['transits'])>0:

            distance=dt['route']['transits'][0]['distance']
            dic['distance']=distance
            walking_distance = dt['route']['transits'][0]['walking_distance']
            dic['walking_distance']=walking_distance
            duration = dt['route']['transits'][0]['duration']
            dic['duration']=duration
            dic['from']=name[0]
            dic['to']=name[1]
            
            print(dic)
            
            dx = pd.DataFrame([dic])
            
            if os.path.exists(out_file):
                dx.to_csv(out_file, mode='a',header=False,index=False)
            else: 
                dx.to_csv(out_file, mode='a',header=True,index=False)
        else:
            print('no route')
            #log
            with open('data/od_log.txt','a') as fl:
                fl.write(f'{name[0]},{name[1]}\n')
    else:
        print(dt['info'])
        get_js(keys,df,num,out_file)
        

def metro_to_metro():
    in_file = 'data/od_metro2metro.json'
    out_file = 'data/od_metro2metro_result.csv'
    
    df = pd.read_json(in_file)
    
    for num in range(0,len(df)):
        print('od_metro2metro',num)
        get_js(keys,df,num,out_file)
    
def metro_to_cbd():
    in_file = 'data/od_metro2cbd.json'
    out_file = 'data/od_metro2cbd_result.csv'
    df = pd.read_json(in_file)
    
    for num in range(len(df)):
        print('od_metro2cbd',num)
        get_js(keys,df,num,out_file)

if __name__ == "__main__":
    os.chdir('data')
    keys = ['99aad79ec1ce59438acbea23a4e840df',
            '8dd06dd6bddfefffdc9e169b00d5191b',
            'ce22dbcb786b2ba113eec2d90e39d497',
            'bdbfe9a35ef43b22d9ade24d09994d4e',
            '238de39355b91ee24029432e241c065c']
    metro_to_cbd()
    metro_to_metro()