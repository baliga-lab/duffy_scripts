#!/usr/bin/Rscript

library('getopt')

spec = matrix(c(
    'verbose', 'v', 2, 'integer',
    'infile', 'i', 1, 'character',
    'outdir', 'o', 1, 'character'
), byrow=TRUE, ncol=4)
opt <- getopt(spec, usage=FALSE)

if (is.null(opt$verbose)) opt$verbose = 0

if (!is.null(opt$infile) && !is.null(opt$outdir)) {
    source('pipelineSetup.R')
    #intable = read.table(opt$infile, sep='\t', header=(opt$useheader == 1))
    intable = read.table(opt$infile, sep='\t', header=TRUE)
    samples <- intable[[1]]
    #pipe.MetaResults(samples, folderName=opt$outdir, annotationFile=opt$infile)
    runMetaResults(folderName=opt$outdir, annotationFile=opt$infile)
} else {
    print(getopt(spec, usage=TRUE))
}
