library(ggplot2)

multMerge = function(mypath){
  filenames = list.files(path = mypath, pattern = "p60 a90.csv", full.names = TRUE)
  datalist = lapply(filenames,
                    function(x){csv <- read.csv(file = x,
                                         header = TRUE,
                                         stringsAsFactors = FALSE)
                        intervalo_s <- dim(csv)[1]
                        intervalo_m <- floor(intervalo_s/60)
                        return(intervalo_m)
                    })
}

a = multMerge("..\\Coletas") #alterar path
df <- data.frame("coleta"=a)
df <- data.frame(t(df))
new_column <- 1:nrow(df)
df <- cbind(new_column, df)
colnames(df)[1] <- "coleta"
colnames(df)[2] <- "lotacao"
print(df)

p10 <- ggplot(df, aes(x = coleta, y = lotacao)) +
        geom_boxplot(fill = "#1f3154", color = "#BC1622", alpha = 0.8,
                     outlier.colour = "#15CB032", outlier.shape = 20) +
        scale_y_continuous(name = "Minutos",
                              breaks = seq(0, 50, 2),
                              limits = c(4, 38))  +
        scale_x_continuous(name = "Coletas")
        ggtitle("Intervalo de tempo das viagens") +
        theme_bw()
plot(p10)