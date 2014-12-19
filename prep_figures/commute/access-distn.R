library(ggplot2)

grab_data <- function(fname) {
  df <- read.table(fname, stringsAsFactors = FALSE)
  colnames(df) <- c("t1", "t2", "time", "count")
  df$cmp <- paste(df$t1, df$t2)
  df$dens <- df$count / sum(df$count)
  df
}

all_equal_shape_5_taxon = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 51, 52, 53, 54, 61, 62, 63, 64, 65, 66, 67, 68, 69)
original_5_taxon <- c(7,14,66,68,69)
n_taxa <- 5; favorite_tangles <- all_equal_shape_5_taxon

n_taxa <- 6; favorite_tangles <- c(662,665,795)

sub_n_taxa <- function(s) sub("NTAXA", as.character(n_taxa), s)
data_of_num <- function(n) {
  df <- grab_data(paste0(as.character(n_taxa),"-taxon-access-distn/equal/",as.character(n),".tab"))
  df$num <- as.factor(n)
  df
}


adjacency <- read.csv(sub_n_taxa("../../rspr/matrix_NTAXA"), header=FALSE)
degree = rowSums(adjacency)
tangles <- read.table(
    sub_n_taxa("../../results-rspr/ricciNTAXA.mat"),
    stringsAsFactors = FALSE)
colnames(tangles) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "coset", "dist", "kappa_str")
tangles$t1_deg <- sapply(tangles$t1_idx, function(i) degree[i+1]) # tangleX.idx uses 0 indexing.
tangles$t2_deg <- sapply(tangles$t2_idx, function(i) degree[i+1]) # tangleX.idx uses 0 indexing.
tangles$coset <- NULL
tangles$num <- c(1:nrow(tangles))
tail(tangles)

d <- do.call(rbind, lapply(favorite_tangles, data_of_num))
d <- subset(d, t1 != t2)
head(d)
d <- merge(d, tangles, by="num")
d$kappa <- sapply(d$kappa_str, function(s) eval(parse(text=s)))
sub_d <- subset(d, t1 < t2)

# Plot in terms of kappa.
p <- ggplot(sub_d, aes(x=time, y=dens, group=num, color=kappa)) + geom_line()
p <- p + scale_x_continuous(limits=c(0,7))
p + facet_grid(dist ~ t1_deg, scales="free")

# Plot showing exponential part of drop.
p <- ggplot(sub_d, aes(x=time, y=dens, group=num, color=factor(t1_deg))) + geom_line()
p <- p + scale_x_continuous(limits=c(0,500)) + scale_y_log10()
p + facet_grid(. ~ dist, scales="free")

p + facet_grid(t1_deg ~ t2_deg)

subset(sub_d, num==66)
