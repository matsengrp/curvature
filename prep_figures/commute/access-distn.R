library(ggplot2)

grab_data <- function(fname) {
  df <- read.table(fname, stringsAsFactors = FALSE)
  colnames(df) <- c("t1", "t2", "time", "count")
  df$cmp <- paste(df$t1, df$t2)
  df$dens <- df$count / sum(df$count)
  df
}

n_taxa <- 5; favorite_tangles <- c(7,14,66,68,69)
n_taxa <- 6; favorite_tangles <- c(662,665,795)
sub_n_taxa <- function(s) sub("NTAXA", as.character(n_taxa), s)
data_of_num <- function(n) {
  df <- grab_data(paste0(as.character(n_taxa),"-taxon-access-distn/",as.character(n),".tab"))
  df$num <- as.factor(n)
  df
}


adjacency <- read.csv(sub_n_taxa("../../rspr/matrix_NTAXA"))
degree = rowSums(adjacency)
tangles <- read.table(
    sub_n_taxa("../../results-rspr/ricciNTAXA.mat"),
    stringsAsFactors = FALSE)
colnames(tangles) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "coset", "dist", "kappa_str")
tangles$t1_deg <- sapply(tangles$t1_idx, function(i) degree[i+1]) # tangleX.idx uses 0 indexing.
tangles$t2_deg <- sapply(tangles$t2_idx, function(i) degree[i+1]) # tangleX.idx uses 0 indexing.
tangles$coset <- NULL
tangles$num <- c(1:nrow(tangles))
head(tangles)

tail(d)
d <- do.call(rbind, lapply(favorite_tangles, data_of_num))
d <- merge(d, tangles, by="num")
sub_d <- subset(d, t1 != t2)
sub_d <- subset(d, t1 < t2)
ggplot(sub_d, aes(x=time, y=count, color=num)) + geom_line() + scale_x_continuous(limits=c(0,25)) + facet_wrap(~ t1_deg)

subset(sub_d, num==66)