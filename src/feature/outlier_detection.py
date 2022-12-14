from src.data.load_data import data

df = data.copy()
df = df.dropna()
# name_list = ['squad-fpp', 'duo', 'solo-fpp', 'squad', 'duo-fpp', 'solo']
# df = df[df["matchType"].isin(name_list) == True]

## start - 박성원
# feature merge
df["total_item"] = df.boosts + df.heals
df["total_distance"] = df.rideDistance + df.walkDistance + df.swimDistance
# boosts
df = df.drop(df[df.boosts>22][df.winPlacePerc<0.2].index)
# total_item
df = df.drop(df[df.winPlacePerc==0][df.total_item>10].index)
# total_distance
df = df.drop(df[df.winPlacePerc==1][df.total_distance==0].index)
df = df.drop(df[df.kills >= 2][df.total_distance == 0].index)
# weaponsAcquired
df = df.drop(df[df.weaponsAcquired>30].index)
df = df.drop(df[df.weaponsAcquired==0][df.winPlacePerc==1].index)
## end - 박성원

## start - 김한길
# 로드디스턴스0 & 로드킬 >0
df=df.drop(index=df[ (df['rideDistance']==0) & (df['roadKills']>0)  ].index)

# 딜이없는데 킬이있는경우
df=df.drop(index=df[ (df['damageDealt']==0) & (df['kills']>0)  ].index)
## end - 김한길

## start - 이채영
# kills, headshotKills, killStreaks, longestKill 이상치 제거 (각 column 별 약 1000개 정도 없어지도록 값을 잡음)
df=df.drop(index=df[ (df['kills']>15) | (df['headshotKills']>7) | (df['killStreaks']>5) | (df['longestKill']>500)  ].index)

# roadKills column 삭제

# df = df.drop('roadKills', axis=1)

## end - 이채영

## start - 김지혜
# DBNOs remove outliers
df.drop(df[df['DBNOs'] > 6].index, inplace= True)

# revives remove outliers
df.drop(df[df['revives'] > 3].index, inplace= True)

# teamkills drop
df=df.drop(['teamKills'],axis=1)
## end - 김지혜

## start - 안희수
df.loc[df.matchType.str.contains('solo'),'solo'] = 1
df.loc[~df.matchType.str.contains('solo'),'solo'] = 0
df.loc[df.matchType.str.contains('duo'),'duo'] = 1
df.loc[~df.matchType.str.contains('duo'),'duo'] = 0
df.loc[df.matchType.str.contains('squad'),'squad'] = 1
df.loc[~df.matchType.str.contains('squad'),'squad'] = 0
df.loc[(df.matchType.str.contains('normal'))|
       (df.matchType.str.contains('crash'))|
       (df.matchType.str.contains('flare')),'event'] = 1
df.loc[(~df.matchType.str.contains('normal'))&
       (~df.matchType.str.contains('crash'))&
       (~df.matchType.str.contains('flare')),'event'] = 0

# row 제거
# remove missing value
# 같은 게임에 참여한 사람 수 컬럼 수 만듦
df['num']=df.groupby('matchId')['Id'].transform('count')
# 한 게임에서 최대 킬수 컬럼
df['max']=df.groupby('matchId')['kills'].transform('max')
# df.loc[df['num']<=df['max'],['num','max']] # 2124 rows

# 최대 킬수가 한 게임 사람 수 보다 많을 수 없음, 행 제거
df=df[df['num']>df['max']]

#한 경기 인원
df.loc[:,'num']=df.groupby('matchId')['Id'].transform('count')

## 참가 인원에 비해 팀 수가 너무 적은 경우 조정
# 팀 수 의 이상치 열 생성
df.loc[:,'numDuo']=df['num']//2
df.loc[:,'numSquad']=df['num']//4

df.loc[df.duo == 1.0,'Gap'] = abs(df['numDuo']-df['numGroups'])
df.loc[df.squad == 1.0,'Gap'] = abs(df['numSquad']-df['numGroups'])
df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0),'Gap']=abs(df['num']-df['numGroups'])

# df['Gap'].value_counts().to_frame().sort_index()

# solo나 event에서 numGroups 이상치 탐색
# df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0),'Gap'].value_counts()
# len(df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0)&(df.Gap>9),'Gap']) # 24907
# print("%.2f" % ((24907/663429)*100)) # 3.75%
# solo나 event인데 Gap이 9보다 큰 경우들 평균값(반올림해서 3)되도록 maxPlace와 numGroup조정
df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0) & (df.Gap > 9),['maxPlace','numGroups']] = df['num']-3

# df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0),'Gap']=abs(df['num']-df['numGroups'])
# df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0),'Gap'].value_counts()


# duo에서 numGroups 이상치 탐색
# df.loc[(df.matchType.str.contains('duo')),['Gap']].value_counts()
# Gap이 5이상 차이 나면 groupId에 문제가 있는 것으로 판단, 사실 그 이하도 문제 존재
# df.loc[(df.matchType.str.contains('duo'))&(df.Gap==5.0),['matchId']].value_counts()
# df.loc[df.matchId== '35c26cc0a5212a','groupId'].value_counts() # 한팀에 2명 이상인 팀 들 5팀 이상
# 보통 API가 꼬인 경우로 보인다. -> Gap이 5이상인 경우 가장 많은 값인 1이 되도록 조정한다.
df.loc[(df.matchType.str.contains('duo'))&(df.Gap>=5),['maxPlace','numGroups']] = df['numDuo']-1

# df.loc[df.duo == 1.0,'Gap']=abs(df['numDuo']-df['numGroups'])
# df.loc[(df.matchType.str.contains('duo')),'Gap'].value_counts()


#squad에서 numgroups이상치 탐색
# df.loc[(df.matchType.str.contains('squad')),['Gap']].value_counts()
# Gap이 8이상 차이 나는 것은 groupId에 이상이 있는 것으로 판단, 사실 그 이하도 문제 존재
# Gap이 8이상인 경우 가장 많은 값인 4가 되도록 조정한다.
df.loc[(df.matchType.str.contains('squad'))&(df.Gap>=8),['maxPlace','numGroups']] = df['numSquad']-4

# df.loc[df.squad == 1.0,'Gap']=abs(df['numSquad']-df['numGroups'])
# df.loc[(df.matchType.str.contains('squad')),'Gap'].value_counts()


## maxPlace가 numGroups와 많이 차이나는 것 조정
df.loc[:,'GrpError']=df['maxPlace']-df['numGroups']
# df.loc[df['GrpError'] > df['GrpError'].quantile(0.99),'GrpError'].value_counts() # 7, 8, 9
# df['GrpError'].mean() # 1.445498e+00

# maxPlace와 numGroups가 많이 차이나는 것(7 이상)은 matchId의 오류로 보고 평균값(반올림해서 2)만큼의 차이를 둬서(maxPlace값 - 2) 조정한다.
df.loc[df.GrpError>=7,'numGroups'] = df['maxPlace']-2

# df.loc[:,'GrpError']=df['maxPlace']-df['numGroups']
# df['GrpError'].value_counts()

# 마지막 확인
# df.loc[df.duo == 1.0,'Gap'] = abs(df['numDuo']-df['numGroups'])
# df.loc[df.squad == 1.0,'Gap'] = abs(df['numSquad']-df['numGroups'])
# df.loc[~(df.duo == 1.0)& ~(df.squad == 1.0),'Gap']=abs(df['num']-df['numGroups'])

# df.loc[df.event ==0.0,'Gap'].value_counts().to_frame().sort_index()

# Gap = 8.0 에서 20명이 존재하는데 이는 matchType이 crash 여서 무시한다.

# 만든열 드랍
df=df.drop(['num', 'max', 'numDuo','numSquad','Gap','GrpError'],axis=1)
## end - 안희수

df = df.drop("killPlace", axis=1)