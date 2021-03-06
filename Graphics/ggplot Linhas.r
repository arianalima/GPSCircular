library("ggplot2")

coleta <- "30"

csv_folder <- "C:\\Users\\Bernardo\\Desktop\\Projetos\\Python\\GPSCircular\\Coletas\\csv's\\coleta "

df1 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p60 a90.csv", sep=""), header = TRUE)
df2 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p60 a150.csv", sep=""), header = TRUE)
df3 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p60 a180.csv", sep=""), header = TRUE)
df4 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p80 a90.csv", sep=""), header = TRUE)
df5 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p80 a150.csv", sep=""), header = TRUE)
df6 <- read.csv(file= paste(csv_folder, coleta, " algoritmo p80 a180.csv", sep=""), header = TRUE)

df1$calculo1_60_150 = df2[match(df1$segundo, df2$segundo),"calculo"]
df1$calculo1_60_180 = df3[match(df1$segundo, df3$segundo),"calculo"] 
df1$calculo1_80_90 = df4[match(df1$segundo, df4$segundo),"calculo"] 
df1$calculo1_80_150 = df5[match(df1$segundo, df5$segundo),"calculo"] 
df1$calculo1_80_180 = df6[match(df1$segundo, df6$segundo),"calculo"]

gg <- ggplot(df1, aes(x=df1$segundo)) +
  geom_line(aes(y = df1$valor_real, colour = "valor_real")) +
  geom_line(aes(y = df1$calculo1_60_150, colour = "calculo1_60_90"))+
  geom_line(aes(y = df1$calculo1_60_150, colour = "calculo1_60_150"))+
  geom_line(aes(y = df1$calculo1_60_180, colour = "calculo1_60_180"))+
  geom_line(aes(y = df1$calculo1_80_90, colour = "calculo1_80_90"))+
  geom_line(aes(y = df1$calculo1_80_150, colour = "calculo1_80_150"))+
  geom_line(aes(y = df1$calculo1_80_180, colour = "calculo1_80_180"))+
  labs(x="Segundos",y="Lota��o",colour = "Valores")
plot(gg)
