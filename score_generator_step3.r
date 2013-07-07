rm(list=ls())

do_corr<-function(X) {
	rez<-cbind(NULL, apply(X,1,mean))
	e<-eigen(X)$vectors[,1]
	r1<-apply(X,1,function(x) e%*%x)
	rez<-cbind(rez, r1)
	rez<-cbind(rez, abs(r1/(max(abs(r1))/max(abs(apply(X,1,mean))))))
	return(rez)
}

do_cooc<-function(X) {
	D<-X%*%t(X)+0.0000000000000000001
	d<-1/sqrt(diag(D))
	N<-D*(d%*%t(d))
	return(do_corr(N))
}

rez<-cbind(NULL,do_corr(as.matrix(read.csv("c:\\temp\\VP2R_TI.csv", header=FALSE))))
rez<-cbind(rez,do_cooc(as.matrix(read.csv("c:\\temp\\VP2R_TI_CO.csv", header=FALSE))))
rez<-cbind(rez,do_corr(as.matrix(read.csv("c:\\temp\\VP2R_AB.csv", header=FALSE))))

## rez<-cbind(rez,do_cooc(as.matrix(read.csv("c:\\temp\\VP2R_AB_CO.csv", header=FALSE))))
rez<-cbind(rez,rep(0,nrow(rez)))
rez<-cbind(rez,rep(0,nrow(rez)))
rez<-cbind(rez,rep(0,nrow(rez)))

rez<-Re(rez)
rez2<-rbind(NULL,apply(rez,2,max))
rez2<-rbind(rez2,apply(rez,2,min))
rez2<-rbind(rez2,apply(rez,2,mean))
rez2<-rbind(rez2,apply(rez,2,sd))
rez<-rbind(rez,rez2)
write.csv(rez,"c:\\temp\\Rout.csv", row.names = FALSE, col.names = FALSE)

q("no")

