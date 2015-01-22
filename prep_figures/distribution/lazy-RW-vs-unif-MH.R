#! /usr/bin/Rscript

library(ggplot2)
library(ape)
library(apTreeshape)

source("process.R")

get_df <- function(n_taxa, walk) {
  d <- get_results(paste0("../../results-rspr/", walk, "/ricci", n_taxa,".mat"))
  d <- sample(d)  # Shuffle rows of d.
  d$n_taxa <- n_taxa
  colnames(d)[colnames(d) == "kappa"] <- paste0("kappa_", walk)
  colnames(d)[colnames(d) == "kappa_str"] <- paste0("kappa_str_", walk)
  d$dist_jitter <- NULL
  d
}

theme_set(theme_bw(16))

n_taxa <- 7
d <- merge(get_df(n_taxa, "lazy_unif"), get_df(n_taxa, "unif_prior_mh"))

p <- ggplot(d, aes(kappa_lazy_unif, kappa_unif_prior_mh, color=t1_nwk))
p <- p + geom_point()
p <- p + scale_x_continuous(name="κ for lazy random walk")
p <- p + scale_y_continuous(name="κ for MH sampling of uniform prior")

ggsave(paste0("kappa", n_taxa, "-lazy-RW-vs-unif-MH.svg"), p, width=9)
