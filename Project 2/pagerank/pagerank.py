import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    resulting_states = dict()
    # if no links available in current page
    if len(corpus[page]) == 0:
        prob = 1/len(corpus)
        for key in corpus.keys():
            resulting_states[key] = prob
        return resulting_states

    # find the damp and random-jump probability
    for key in corpus.keys():
        damp_prob = 0
        if key in corpus[page]:
            damp_prob = damping_factor * (1/len(corpus[page]))
        rand_prob = (1-damping_factor) * (1/len(corpus))
        total_prob = damp_prob + rand_prob
        resulting_states[key] = total_prob

    return resulting_states 


# helper function for sample_pagerank function
# decides the next page for the given current page
def findNextPage(transitions):
    cumulativeProb = 0
    r = random.random()
    for (page, prob) in transitions.items():
        cumulativeProb += prob
        if r < cumulativeProb:
            return page

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initially stores the count of page visits, later the page rank
    pagerank = {page: 0 for page in corpus.keys()}

    # select a random initial page
    current_page = random.choice(list(corpus.keys()))
    pagerank[current_page] += 1

    # loop to find the next n-1 samples 
    for i in range(n-1):
        transitions = transition_model(corpus, current_page, damping_factor)
        next_page = findNextPage(transitions)
        pagerank[next_page] += 1
        current_page = next_page
    
    # converting the page visits to % based on total visits
    for page in pagerank.keys():
        pagerank[page] /= n

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initializing a dictionary for every page
    n = len(corpus)
    # filling page rank by 1/N
    pagerank = {key: 1/n for key in corpus.keys()}
    # loop that tracks if any acceptable change has occurred
    acceptable_change = True
    while(acceptable_change):
        acceptable_change = False
        new_rank = pagerank.copy()
        for page in pagerank:
            # damp probability
            damp_prob = 0
            for i in pagerank.keys():
                if len(corpus[i]) == 0:
                    damp_prob += pagerank[i]/n 
                elif page in corpus[i]:
                    damp_prob += (pagerank[i]/len(corpus[i])) 
            damp_prob *= damping_factor
            # random-jump probability
            rand_prob = (1-damping_factor) / n
            new_rank[page] = damp_prob + rand_prob
            # checking if there a was a change to continue looping
            if abs(new_rank[page] - pagerank[page]) > 0.001:
                acceptable_change = True
        pagerank = new_rank
    return pagerank

if __name__ == "__main__":
    main()
