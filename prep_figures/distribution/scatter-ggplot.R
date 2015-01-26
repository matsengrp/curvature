library(ggplot2)
library(ape)
library(apTreeshape)

source("process.R")

theme_set(theme_bw(22))

n_taxa <- 7
# walk <- "lazy_unif"; sub_title <- " taxa, lazy uniform random walk"
walk <- "unif_prior_mh"; sub_title <- " taxa, uniform prior MCMC"

d <- get_results(paste0("../../results-rspr/", walk, "/ricci", n_taxa,".mat"))

p <- ggplot(d, aes(kappa, dist_jitter, color=avg_sackin))
p <- p + geom_point()
p <- p + ggtitle(paste0(n_taxa, sub_title))
p <- p + scale_x_continuous("κ") + scale_y_continuous("SPR distance")
p <- p + scale_colour_gradient(name="Sackin\nmeasure\n",
                         breaks=c(min(d$avg_sackin), max(d$avg_sackin)),
                         labels=c("balanced", "imbalanced"))

ggsave(paste0("scatter-ricci-", walk, "-",n_taxa,".svg"), p, width=9.5, height=7)
 