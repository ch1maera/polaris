required.packages <- c("data.table", "jsonlite", "dplyr", "ggplot2", "zoo", "ggthemes")

needed.packages <- required.packages[!(required.packages %in% installed.packages()[,"Package"])]

if (length(needed.packages)){
install.packages(needed.packages)
}

library(data.table)
library(jsonlite)
library(dplyr)
library(ggplot2)
library(ggthemes)
library(zoo)

## ESI url segments to fetch data
ESI_BASE = "https://esi.tech.ccp.is/latest/"
ESI_SOURCE = "?datasource=tranquility"

## Regions that have NPC corps that accept Blue Loot buy orders
regionIDs <- c(10000054,10000001,10000036,10000043,10000064,10000037,
  10000067,10000011,10000030,10000052,10000065,10000016,
  10000042,10000028,10000041,10000020,10000033,10000002)

## Type IDs for the four blue loot items, and their NPC values, dropped by Sleepers in wormholes
typeIDs <- c(30746,30744,30745,30747)
buyorder <- c(1500000,200000,500000,5000000)


all.loot <- data.frame(date=as.Date(character()), regionID=numeric(), typeID=numeric(),order_count=integer(), volume=integer(),value=numeric())


for(k in 1:4){
	for(i in regionIDs){
		volumeHistory_addr = paste0(ESI_BASE,"markets/",i,"/history/",ESI_SOURCE,"&type_id=",typeIDs[k])
		volume.json <- fromJSON(readLines(volumeHistory_addr))
		volume.json.data <- data.table(volume.json)
		volume.data <- volume.json.data[,list(date=as.Date(date),regionID=i, typeID=typeIDs[k],order_count=order_count,volume=volume,value=volume*buyorder[k])]
		all.loot <- rbind(all.loot,volume.data)
	}
}

##Aggregating Regional Data
all.loot.value <-group_by(all.loot,date)
all.loot.value <-summarise(all.loot.value,value=sum(value))
all.loot.value$average <- rollmean(all.loot.value$value,14,align='right',fill=NA)

##Creating Plot
plot <- ggplot(all.loot.value,aes(x=all.loot.value$date)) +
	geom_line(aes(y=all.loot.value$value),color='black') +
	geom_line(aes(y=all.loot.value$average),color='red',size=1) +
	scale_y_continuous(breaks=c(2e+11,4e+11,6e+11,8e+11),labels=c("200b","400b","600b","800b")) +
	ggtitle("Blue Loot Sales In New Eden") +
	geom_vline(xintercept=as.numeric(as.Date("2017-07-11")),linetype=4) +
	theme_fivethirtyeight()

plot

plot.height=900
plot.width=1600
chart_path=paste0(getwd(),"\\Plots\\")
dir.create(chart_path, showWarnings=FALSE)

##Saving PNG of Plot To Disk
png(paste0(chart_path,"BlueLootSales.png"),width=plot.width,height=plot.height)
print(plot)
dev.off()

##Saving CSV Files to Disk
write.csv(all.loot,paste0(chart_path,"AllLoot",Sys.Date(),".csv"), row.names=FALSE)
write.csv(all.loot.value,paste0(chart_path,"AggregateValue",Sys.Date(),".csv"),row.names=FALSE)
