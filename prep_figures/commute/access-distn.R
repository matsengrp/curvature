library(dplyr)
library(ggplot2)
library(magrittr)

theme_set(theme_bw(16))

grab_data <- function(fname) {
  df <- read.table(fname, stringsAsFactors = FALSE)
  colnames(df) <- c("t1", "t2", "time", "count")
  df$cmp <- paste(df$t1, df$t2)
  df$dens <- df$count / sum(df$count)
  df
}

original_5_taxon <- c(7,14,66,68,69)
all_equal_shape_5_taxon <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 51, 52, 53, 54, 61, 62, 63, 64, 65, 66, 67, 68, 69)
all_5_taxon <- 1:69
n_taxa <- 5; favorite_tangles <- all_5_taxon
data <- "123_45-1v5c/"
data <- "123_45-equal/"

all_equal_shape_6_taxon <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 662, 665, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 776, 777, 778, 779, 780, 781, 782, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807)
original_6_taxon <-  c(662,665,795)
all_6_taxon <- 1:807
n_taxa <- 6; favorite_tangles <- all_6_taxon
data <- "equal/"
data <- "123_456-equal/"
data <- "123_456-1v5c/"

sub_n_taxa <- function(s) sub("NTAXA", as.character(n_taxa), s)
data_of_num <- function(n) {
  cat(n)
  df <- grab_data(paste0(as.character(n_taxa),"-taxon-access-distn/",data,as.character(n),".tab"))
  df$num <- as.numeric(n)
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


# Calculate the expectation of the commute time,
# (compare below where we are looking at the complete distribution).
expectations <- d %>%
  group_by(num) %>%
  summarise(expectation = sum(time*dens))
expectations <- merge(expectations, tangles, by="num")

p <- ggplot(expectations, aes(x=expectation))
p <- p + geom_histogram(binwidth=1) + labs(title=paste(n_taxa, "taxon access times"))
p <- p + facet_grid(t1_deg ~ t2_deg) + scale_x_continuous(labels = function (x) floor(x))
p + theme(panel.grid.minor =   element_blank(),
          panel.grid.major =   element_line(size=1.))
ggsave(paste0(n_taxa,"-taxon-access-by-degree.svg"))

# There are two entries for each (num, time) pair for the two directions,
# assuming as we do that the trees are distinct.
# Here we average their densities.
# Alternatively, we could look at the two times individually,
# but they are the same in the limit of lots of samples.
means <- d %>%
  group_by(num, time) %>%
  summarise(mean_count = mean(count))
d <- merge(d, means)
# Because we are looking at means, we only take one representative.
d <- subset(d, t1 < t2)


# Plot in terms of kappa.
p <- ggplot(d, aes(x=time, y=mean_count, group=num, color=kappa, fill=kappa))
p <- p + geom_line()
p <- p + scale_x_continuous(limits=c(0,4)) + scale_y_log10()
p + facet_grid(dist ~ t1_deg, scales="free")

# Plot showing exponential part of drop.
p <- ggplot(d, aes(x=time, y=dens, group=num, color=t1_deg)) + geom_smooth()
p <- p + scale_x_continuous(limits=c(0,500)) + scale_y_log10()
p + facet_grid(. ~ dist, scales="free")

p + facet_grid(t1_deg ~ dist)

p + facet_grid(t1_deg ~ t2_deg)


# Plot showing exponential part of drop.
p <- ggplot(sub_d, aes(x=time, y=dens, group=num, color=factor(t1_deg))) + geom_line()
p <- p + scale_x_continuous(limits=c(0,500)) + scale_y_log10()
p + facet_grid(. ~ dist, scales="free")

p + facet_grid(t1_deg ~ t2_deg)

subset(sub_d, num==66)

d <- subset(d, num==10)
