from src.feature.outlier_detection import df

df_corr = df.corr()

from scipy import stats
df["score1"] = df.damageDealt*13 + df.assists*8 + df.kills*9 \
               + df.longestKill*4 + df.killStreaks*2 + df.boosts*10\
               + df.heals*6 + df.DBNOs*4 + df.revives*2
stats.ttest_ind(df.score1,df.winPlacePerc,equal_var=False)