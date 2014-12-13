library(ape, apTreeshape)

shape_of_str <- function(s) as.treeshape(read.tree(text=s))


get_results <- function(path) {
    d <- read.table(path, stringsAsFactors=FALSE)
    colnames(d) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "mult", "dist", "kappa_str")
    d$row = 1:nrow(d)
    d <- subset(d, kappa_str != "-")
    d$kappa <- sapply(d$kappa_str, function(s) eval(parse(text=s)))
    d$info= paste(d$t1_nwk, d$t2_nwk, paste("kappa:", d$kappa_str), sep="<br />")
    d$dist_jitter = d$dist + runif(nrow(d), min = -0.35, max = 0.35)

    # Tree shape information.
    d$t1_shape <- lapply(d$t1_nwk, shape_of_str)
    d$t2_shape <- lapply(d$t2_nwk, shape_of_str)
    d$t1_colless <- sapply(d$t1_shape, colless)
    d$t2_colless <- sapply(d$t2_shape, colless)

    d
}




