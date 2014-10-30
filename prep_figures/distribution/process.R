
get_results <- function(path) {
    d <- read.table(path, stringsAsFactors=FALSE)
    colnames(d) <- c("t1_idx", "t2_idx", "t1_nwk", "t2_nwk", "mult", "dist", "kappa_str")
    d <- subset(d, kappa_str != "-")
    d <- sample(d)  # Shuffle rows of d.
    d$kappa <- sapply(d$kappa_str, function(s) eval(parse(text=s)))
    d$info= paste(d$t1_nwk, d$t2_nwk, paste("kappa:", d$kappa_str), sep="<br />")
    d$dist_jitter = d$dist + runif(nrow(d), min = -0.35, max = 0.35)
    d
}
