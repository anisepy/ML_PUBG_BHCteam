# PUBG 승률 예측 머신러닝 모델링 프로젝트 

- [PUBG Finish Placement Prediction - Kaggle](https://www.kaggle.com/competitions/pubg-finish-placement-prediction)

## 개요

캐글 대회였던 PUBG 최종 승자 예측의 데이터를 활용하여 배그 초보자들에게 고수들이 어떻게 행동하는지를 데이터 근거와 함께 조언을 주려는 목적으로 프로젝트를 진행하였습니다.

> PUBG란? : PlayerUnknown's Battel Grounds, 배틀그라운드라는 이름의 배틀로얄 방식의 게임, 100명의 플레이어가 비행기에서 뛰어내려 무기를 파밍하고 마주치면 싸우면서 제거, 강탈하며 최후의 1인(혹은 한팀)이 살아남을 때까지 진행하는 게임. 블루존(Blue Circle) 안에서 경기가 진행되며 이 밖에서는 자기장에 의해 사망합니다. 데이터(2018.8.5)는 PUBG Developer API에 의해 구성되었으며, 65000게임의 플레이어 데이터를 트레이닝과 테스트 용으로 나뉘어져 있습니다.

![PUBG](https://img.seoul.co.kr/img/upload/2022/01/12/SSI_20220112152324_O2.jpg)

## EDA

### 1. 데이터 개요

- 연속형 변수 : 이동거리(차량,도보,수영), 데미지피해량, 장거리킬 거리, 승률
- 이산형 변수 : 킬 수, 어시스트 수, 아이템 사용수, 등수, 매치 시간, 무기 획득 수, 랭크 포인트 등..
- 문자형 데이터 : 매치 유형, ID, 매치ID 등..
- 예측 타겟(y) : WinPlacePerc(승률)

![winplaceperc](https://user-images.githubusercontent.com/103994044/182508295-e8a9052d-f610-4884-963e-fb7b857236fe.png)

### 2. 게임 형태 분석

- matchType feature에는 6가지의 일반 게임 타입과 10가지의 custom 게임 타입이 있습니다. 이렇게 2가지 분류로 나누어 분석한 결과 이동거리 대비 아이템 사용에서 유의미한 결과를 찾았습니다. custom 게임의 경우 일반 게임보다 이동거리가 대체적으로 짧았고 아이템 사용이 적었습니다. 이는 custom 게임의 경우 경기의 조건 등을 특정하게 되고, 목적성에 맞게 전투가 일어나서 경기 자체가 컴팩트하게 진행되어서 이런 데이터가 나온 것으로 분석됩니다.
- 이를 반영하여 매치 타입을 one-hot encoding으로 쪼개서 머신러닝의 feature로 추가하였습니다.

<img width="499" alt="item distance" src="https://user-images.githubusercontent.com/103994044/182531019-2b70734e-eb83-4bb6-89aa-2423279405be.png">

- matchDuration과 총 아이템 사용을 비교해보니 경기시간의 1600초 대에서 경계가 보였습니다. 이는 맵사이즈에 따라서 경기시간이 차이난 것으로 분석됩니다.
- 따라서 이 기준에 맞게 맵크기에 대한 feature를 추가하였습니다.

<img width="482" alt="matchduration" src="https://user-images.githubusercontent.com/103994044/182530935-e1fc6284-c62b-4e45-abdc-021074eae604.png">

### 3. 고수 판별

- 데이터 만을 가지고 고수를 판별하기 위해 여러가지 시도를 해보았습니다. 그중에 타겟인 `WinPlacePerc`을 이용하여 상위 10% 중위 80% 하위 10%를 나누어 이동거리, 아이템 사용수, 무기 습득 수를 barplot을 통해 비교하였습니다.

<img width="973" alt="lmt" src="https://user-images.githubusercontent.com/103994044/182530970-4d4c712f-e87c-4ab3-8f94-308acbed44d8.png">

- 하지만 상위 10% = 고수 일거라는 추측에 불가하므로 조금 더 근거가 필요했습니다. 그래서 dak.gg의 상위 랭커들의 데이터를 크롤링 해서 나온 특징들을 조합하여 원본 데이터와 비교한 결과 확실한 근거를 잡을 수 있었습니다. 왼쪽이 크롤링한 데이터의 특징이 반영된 원본데이터의 고수들 분포 수 입니다.

<img width="725" alt="highranker" src="https://user-images.githubusercontent.com/103994044/182530998-7dee90b5-4bef-4b11-897a-d16e685ad2fd.png">

- 조금 더 세분화 하여 각 feature에서 고수들은 어떤 행동 형태를 보이는지 분석 했습니다. 
- 고수들은 이동할때 주로 차량으로 이동해서 불필요한 도보 이동을 줄이는 것으로 보입니다. 

![distance-hl](https://user-images.githubusercontent.com/103994044/182524049-ef6c2d7b-50be-453b-a640-b1fbce291d70.png)

- 불필요한 이동을 줄이고 좋은 자리를 선점해서 장거리 킬로 안전확보, 불필요한 킬을 하지 않고 생존률을 높이는 행동 형태를 보입니다.
- 이는 무기의 종류에서도 확인할 수 있습니다. 고수들이 선호하는 총은 mini14, HK416, MK12, Kar98k 등 원거리 사격에 적합한 총(SR)들입니다.

![kill-hl](https://user-images.githubusercontent.com/103994044/182524027-769ed991-5c58-472a-adbd-6b4d335ad1cd.png)

- 이렇게 불필요한 행동을 하지 않고 전략적으로 움직이다 보니 힐 아이템 사용 수는 적고, 부스트 아이템 사용 수 가 많습니다.

<img width="905" alt="feature생성" src="https://user-images.githubusercontent.com/103994044/182533899-6608b4d9-8a18-475f-bf4b-3c56bde9a941.png">
- 분석한 EDA 결과를 바탕으로 추가하려는 feature 입니다. 이 feature가 추가됨으로써 머신러닝의 예측값이 좋아진다면 저희의 가설이 옳다는 증명이 될 것입니다.

### 4. 이상치 삭제

- 정상적인 게임에서 나올 수 없는 데이터들을 행삭제 하였습니다. 
> WinPlacePerc에 있는 결측치
> 
> 이동이 없는데 kill수 존재
> 
> 한 매치에서 최대 킬 수가 해당 매치의 참여인원수 보다 많은 경우
> 
> 차량 탄 거리가 0인데 roadkill 이 1 이상인 경우
> 
> ...

- 값들이 너무 크거나 너무 작아서 ML모델 성능에 영향을 줄 것으로 판단되는 경우도 삭제하였습니다.

## Feature Engineering

- 위에서도 추가한 feature에 대해서 설명했지만 추가적으로 각 매치의 전체 수치에 대한 비율, 평균, 최대값, 순위화 피쳐 들과 EDA결과를 적용한 피쳐들을 만들었습니다.
- 아래는 모델링이 전부 진행한 뒤 뽑아본 feature들의 중요도를 나타내었습니다.

![feature-hl](https://user-images.githubusercontent.com/103994044/182524064-1cee02a2-cf2b-41b5-8b0e-603e75b84d8b.png)

## Modeling

<img width="644" alt="스크린샷 2022-08-03 오후 3 12 21" src="https://user-images.githubusercontent.com/103994044/182536931-86b406c3-4ccd-4dd6-8b7b-c9ac1b78d57e.png">

- 캐글 대회에서는 평가지표로 데이터에 이상치가 많아서 이상치에 상대적으로 rmse, mse보다 둔감한 mae를 평가지표로 캐글이 지정했다고 추정됩니다.
- 저희는 트리기반 모델 중 데이터 양이 많을 때, 효율적이고 학습 능력이 좋은 Xgboost,LightGBM,catboost 모델들을 학습에 사용하였습니다.
- 그 중 catboost를 사용했을 때 mae가 가장 작았습니다. 이는 안에 내장된 딥러닝의 뉴럴네트워크를 모방한 방식이 다른 모델보다 더 우수한 학습 성능을 만들었다고 생각합니다. 
- 크롤링한 결과를 바탕으로 만든 고수들의 행동지표가 반영된 feature가 추가되었을때 MAE값이 개선되었음을 확인했습니다. 이를 통해 저희가 EDA 과정 중에 새운 가설이 맞다고 증명할 수 있습니다.
- hyper-parameter는 optuna를 통해 찾아내어 적용하였습니다. 추가적으로 랜덤포레스트와 xgboost, light gbm 등을 스태킹 하고 메타 모델로 catboost를 쓴 결과가 catboost단일로 모델링 한 것보다 수치가 좋지 않아서 앙상블은 제외하였습니다.
- 아쉬운 점은 상위랭커 크롤링 데이터 밖에 없어서, 상위등수만 잘 맞추는 feature이다 보니 균등하게 적용하기는 부족하지 않았나 싶습니다. 중위 하위 플레이어에 대한 추가지표가 있었으면 더 유의미한 feature를 만들 수 있었을 것이란 아쉬움이 있습니다.

## 결론

- 저희는 이런 결과를 바탕으로 배그 초보자들에게 줄 수 있는 조언 4가지를 뽑았습니다.

> 첫째, 수영하지 말고 부스트탬을많이 사용하고 차량이동을 하여 좋은 자리를 선점하세요.
>
> 둘째, 적만 보면 달려들어서 개죽음 당하는 일이 없도록하세요
>
> 셋째, 엄폐물을 잘 활용하세요 잘 숨는게 운용이고 생존이지 겁쟁이가 아닙니다.
>
> 마지막, 자신의 자리는 저격으로 완성됩니다. 스나이핑을연습하세요
