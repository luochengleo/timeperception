require(ordinal)
mydata = read.table("data.tsv",head=TRUE)

fm1 <- clm(as.factor(perceived_ratio_bin) ~ userid * relevant_before * taskid * estimation, data=mydata)