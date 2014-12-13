library(ape, apTreeshape)

shape_of_str <- function(s) as.treeshape(read.tree(text=s))


get_results <- function(path) {
    d <- read.table(path, stringsAsFactors=FALSE)
    # colnames(d) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "dist", "kappa", "MAT", "MCT") # no stderr
    colnames(d) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "dist", "kappa", "MAT", "MAT_stderr", "MCT", "MAT_stderr")
    d$info= paste(d$t1_nwk, d$t2_nwk, sep="<br />")

    # Tree shape information.
    d$t1_shape <- lapply(d$t1_nwk, shape_of_str)
    d$t2_shape <- lapply(d$t2_nwk, shape_of_str)
    d$t1_colless <- sapply(d$t1_shape, colless)
    d$t2_colless <- sapply(d$t2_shape, colless)

    d
}
