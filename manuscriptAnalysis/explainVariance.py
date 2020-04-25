import numpy as np
from subprocess import call
import sys
from keras.models import load_model

# sequence
from joint_embeddings import get_embeddings_low_mem
from sequence_interpretation import plot_multiplicity, plot_kmer_scores, plot_correlation, plot_dots
from sequence_interpretation import motifs_in_ns, second_order_motifs
from sequence_attribution import get_sequence_attribution

# chromatin
from chromatin_interpretation import scores_at_domains
from chromatin_interpretation import scores_at_states, seq_scores_at_states
from chromatin_interpretation import make_heatmap_per_quartile
from chromatin_interpretation import plot_compensation

# hills
from findhills import find_hills


def plot_seq_figures(datapath, model, out_path, no_of_chrom_datasets):
    """
    Uses a trained NN, and plots manuscript figures that explain sequence figures.

    Parameters:
        datapath (str): Prefix to the data files.
        model (keras Model): trained model in '.hdf5' format.
        outpath (str): Directory to store output files + figs.

    Returns: None
        Saves all output files + figures in the output directory
    """
    # Load the bound sequences
    seq_data = np.load(datapath + '.bound.seq.npy')
    chromatin_data = np.load(datapath + '.bound.chromtracks.npy')
    call(['mkdir', out_path])


    # Currently NOT using this functionality for the main figures.
    # Getting sequence attribution
    # grad, grad_star_inp = get_sequence_attribution(datapath, model, (seq_data, chromatin_data),
    #                                                no_of_chrom_datatracks=no_of_chrom_datasets)

    grad_star_inp = np.load(out_path + 'gradients_star_inp.npy')
    # this saves a '.hills' file with event locations
    find_hills(grad_star_inp=grad_star_inp, datapath=datapath, out_path=out_path)


    # np.save(out_path + "gradients", grad)
    # np.save(out_path + "gradients_star_inp", grad_star_inp)
    # rb_attribution = np.load(out_path + "sequence_attribution.npy")
    # visualize(datapath, out_path, input_data, rb_attribution)

    # Plot frequencies of 'CAGSTG' k-mers
    # embedding = get_embeddings_low_mem(model, seq_input=seq_data,
    #                                    chrom_input=chromatin_data)

    outfile_a = out_path + '4a.pdf'
    outfile_b = out_path + '4b.pdf'
    # canonical motifs (?) ## CHECK THIS?
    motifs = ['CAGCTG', 'CACCTG', 'CAGGTG']
    # Plot correlations between # of motifs and scores.
    # plot_correlation(datapath, embedding, (seq_data, chromatin_data),
    #                  outfile_a, outfile_b, motifs)

    # Plot correlations between # of SIMULATED motifs and scores.
    outfile = out_path + '4c.pdf'
    no_of_repeats = 1000
    motif = 'CAGCTG'  # Using the most frequent motif here.
    # plot_multiplicity(model, motif, outfile, no_of_repeats)

    # Embed all 10-mers in SIMULATED data; aggregate results over 8-mers
    scores_file = out_path + '10mer.kmer_scores.txt'
    outfile = out_path + '4d.pdf'
    # Removing any pre-existing 'scores_file', function uses file appending.
    # call(['rm', scores_file])
    # motifs = ['CAGCTG', 'CACCTG']
    # for motif in motifs:
    #     second_order_motifs(scores_file, model, motif=motif)
    # print "Plotting scores at kmers + 2bp flanks"
    # plot_kmer_scores(scores_file, outfile)

    # Embed all 8-mer/10-mer k-mers in a background of Ns
    # Calculate scores for 'CAGSTG kmer + 1bp flanks' in SIMULATED sequences
    scores_file = out_path + '8mer.Ns.kmer_scores.txt'
    outfile = out_path + '4e.pdf'
    # call(['rm', outfile])
    # for motif in motifs:
    #     motifs_in_ns(scores_file, model, motif=motif)
    # print "Plotting scores at kmers + 1bp flanks"
    # plot_dots(scores_file, outfile)


def interpret_chromatin(datapath, model, out_path):
    """
    Takes as input a model and the datapath to produce average
    chromatin score over domains.
    ----
    # Additional Requirements:
    # I need a file called datapath + '.domains'
    # This file should contain the domain calls mapped to the test chromosome
    # Currently, the domain caller used is in JAVA, so require a pre-processed file here.
    # This pre-processed file is loaded by the function itself.
    ----
    Produces a box plot in a sub-folder called datapath + Figure4
    Also, split the bedfiles based on chromatin scores
    """
    # Load the input data
    # Load the bound sequences
    # seq_data = np.load(datapath + '.bound.seq.npy')
    # chromatin_data = np.load(datapath + '.bound.chromtracks.npy')

    # make the output directory
    call(['mkdir', out_path])

    # make_heatmap_per_quartile(datapath, out_path=out_path)
    plot_compensation(datapath, out_path=out_path)

    # calculating scores at chromatin input track domains..
    # scores_at_domains(model, datapath, out_path)
    # sum_heatmap(datapath, input_data, out_path)
    # calculating chromatin scores at chromHMM states"
    # order = scores_at_states(model, datapath, out_path)
    # print "Calculating sequence scores at chromHMM states"
    # seq_scores_at_states(model, datapath, input_data, out_path, order)


def main():

    datapath = sys.argv[1]
    model = sys.argv[2]
    outpath = sys.argv[3]
    no_of_chrom_datasets = 13

    model = load_model(model)

    # sequence_attribution(args.datapath, model)
    plot_seq_figures(datapath=datapath, model=model, out_path=outpath,
                     no_of_chrom_datasets=no_of_chrom_datasets)

    # interpret_chromatin(datapath=datapath, model=model, out_path=outpath)


if __name__ == "__main__":
    main()