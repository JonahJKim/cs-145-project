from zhipuai import ZhipuAI
import os

API_KEY = os.getenv("API_KEY")
client = ZhipuAI(api_key=API_KEY)

xml_paper = """
<?xml version="1.0" encoding="UTF-8"?>
<TEI xml:space="preserve" xmlns="http://www.tei-c.org/ns/1.0" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.tei-c.org/ns/1.0 https://raw.githubusercontent.com/kermitt2/grobid/master/grobid-home/schemas/xsd/Grobid.xsd"
 xmlns:xlink="http://www.w3.org/1999/xlink">
	<teiHeader xml:lang="en">
		<fileDesc>
			<titleStmt>
				<title level="a" type="main">Automated Unsupervised Graph Representation Learning</title>
			</titleStmt>
			<publicationStmt>
				<publisher/>
				<availability status="unknown"><licence/></availability>
			</publicationStmt>
			<sourceDesc>
				<biblStruct>
					<analytic>
						<author>
							<persName><forename type="first">Zhenyu</forename><surname>Hou</surname></persName>
						</author>
						<author>
							<persName><forename type="first">Yukuo</forename><surname>Cen</surname></persName>
						</author>
						<author>
							<persName><forename type="first">Yuxiao</forename><surname>Dong</surname></persName>
						</author>
						<author>
							<persName><forename type="first">Jie</forename><surname>Zhang</surname></persName>
						</author>
						<author>
							<persName><forename type="first">Jie</forename><surname>Tang</surname></persName>
						</author>
						<author>
							<persName><forename type="first">Ieee</forename><surname>Fellow</surname></persName>
						</author>
						<title level="a" type="main">Automated Unsupervised Graph Representation Learning</title>
					</analytic>
					<monogr>
						<imprint>
							<date/>
						</imprint>
					</monogr>
				</biblStruct>
			</sourceDesc>
		</fileDesc>
		<encodingDesc>
			<appInfo>
				<application version="0.7.2" ident="GROBID" when="2022-12-25T14:13+0000">
					<desc>GROBID - A machine learning software for extracting information from scholarly documents</desc>
					<ref target="https://github.com/kermitt2/grobid"/>
				</application>
			</appInfo>
		</encodingDesc>
		<profileDesc>
			<textClass>
				<keywords>
					<term>Representation learning</term>
					<term>Graph embedding</term>
					<term>Graph filter</term>
				</keywords>
			</textClass>
			<abstract>
<div xmlns="http://www.tei-c.org/ns/1.0"><p>Graph data mining has largely benefited from the recent developments of graph representation learning. Most attempts to improve graph representations have thus far focused on designing new network embedding or graph neural network (GNN) architectures. Inspired by the SGC and ProNE models, we instead focus on enhancing any existing or learned graph representations by further smoothing them via graph filters. In this paper, we introduce an automated framework AutoProNE to achieve this. Specifically, AutoProNE automatically searches for a unique optimal set of graph filters for any input dataset, and its existing representations are then smoothed via the selected filters. To make AutoProNE more general, we adopt self-supervised loss functions to guide the optimization of the automated search process. Extensive experiments on eight commonly used datasets demonstrate that the AutoProNE framework can consistently improve the expressive power of graph representations learned by existing network embedding and GNN methods by up to 44%. AutoProNE is also implemented in CogDL, an open source graph learning library, to help boost more algorithms.</p></div>
			</abstract>
		</profileDesc>
	</teiHeader>
	<text xml:lang="en">
		<body>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="1">INTRODUCTION</head><p>G RAPHS have been commonly used for modeling structured and relational data, such as social networks, knowledge graphs, and biological networks. Over the past few years, mining and learning with graph data have been shifted from structural feature engineering to graph representation learning, which offers promising results in various applications, including node classification <ref type="bibr" target="#b0">[1]</ref>, recommender system <ref type="bibr" target="#b1">[2]</ref>, and machine cognitive reasoning <ref type="bibr" target="#b2">[3]</ref>.</p><p>Broadly, research on graph representation learning can be grouped into two categories: unsupervised network embedding methods and graph neural networks (GNNs). The network embedding methods aim to project the structure of a network into a latent low-dimensional space such as its structural properties are encoded in the latent vectors. Usually, the input to them contains only the graph topology without input features. Representative network embedding models include skip-gram based methods such as DeepWalk <ref type="bibr" target="#b3">[4]</ref>, LINE <ref type="bibr" target="#b4">[5]</ref>, and node2vec <ref type="bibr" target="#b5">[6]</ref> as well as matrix factorization based methods such as HOPE <ref type="bibr" target="#b6">[7]</ref>, and NetMF <ref type="bibr" target="#b7">[8]</ref>.</p><p>Graph neural networks (GNNs) on the other hand usually take both node/edge features and graph structures as the input and iteratively aggregate neighbors' features to update each node's representation. Most early GNN models are end-to-end (semi) supervised frameworks with the label information for optimization, such as the graph convolutional network (GCN) <ref type="bibr" target="#b0">[1]</ref> and graph attention network (GAT) <ref type="bibr" target="#b8">[9]</ref>. Recently, self-supervised graph neural networks gain significant attention due to their enormous</p><p>• Zhenyu Hou, Yukuo Cen and Jie Zhang are with the Department of Computer Science and Technology, Tsinghua University, China. Email:{houzy21, cyk20, j-z16}@mails.tsinghua.edu.cn. • This work was done when Yuxiao Dong was at Microsoft Research, Redmond, and he is now at Facebook AI, USA. Email: ericdongyx@gmail.com • Jie Tang is with the Department of Computer Science and Technology, Tsinghua University, and Tsinghua National Laboratory for Information Science and Technology (TNList), China. E-mail: jietang@tsinghua.edu.cn, corresponding author.</p><p>potential in shaping the future of graph mining and learning. For example, the GraphSage model <ref type="bibr" target="#b9">[10]</ref> with the unsupervised loss can be considered as a self-supervised framework. DGI <ref type="bibr" target="#b10">[11]</ref> and GCC <ref type="bibr" target="#b11">[12]</ref> leverage the idea of contrastive learning <ref type="bibr" target="#b12">[13]</ref>, <ref type="bibr" target="#b13">[14]</ref> to pre-train graph neural networks via self-supervised signals from the unlabeled input data. Among the exciting progress in graph representation learning, two recent developments are particularly attractive. First, Wu et al. <ref type="bibr" target="#b14">[15]</ref> discover that the non-linearity between GCN layers can be simplified, based on which the SGC model without nonlinearity is proposed. By removing the non-linearity, it is easy to decouple the feature transformation and propagation steps in GCNs' neighborhood aggregation process, enabling us to design these two steps separately. The second one is the ProNE model, in which Zhang et al. <ref type="bibr" target="#b15">[16]</ref> show that using a modulated Gaussian filter to propagate/smooth the node embeddings can significantly improve the expressive power of the embeddings.</p><p>Inspired by these two works, we propose to study whether we can improve graph representation learning by focusing on the propagation step, that is, given the input embeddings such as learned by DeepWalk or DGI, the goal is to further enhance their expressive power by propagating/smoothing the embeddings. First, instead of relying on label information, we are interested in techniques that can benefit graph representation learning in an unsupervised or self-supervised manner. Second, rather than a fixed Gaussian filter, we would like to answer the question of whether there exist better graph filters for propagating existing embeddings. Finally, the natural need is to avoid the manual design or choice of graph filters for each dataset, that is, can we automatically find the best filters for each specific graph? Solutions. To address these issues, we present the AutoProNE framework to automatically find the appropriate graph filters to smooth existing graph representations in a self-supervised manner. Different from ProNE that uses a fixed Gaussian kernel for all graphs, the proposed framework leverages the idea of AutoML AutoML Fig. <ref type="figure">1</ref>. The Overview of the AutoProNE Framework. The input is the node embeddings learned by any other network embedding or GNN methods and the output is the smoothed embeddings with enhanced expressive power. AutoProNE includes two components: <ref type="bibr" target="#b0">(1)</ref> Parameter selection: the AutoML parameter generator automatically select graph filters and corresponding hyperparameters. (2) Embedding propagation: once the graph filters are selected, they are used to smooth the input embeddings. In the example, the PPR and Gaussian graph filters as well as their parameters are selected for the specific input graph. And as a result, each node pays attention to its indirect neighbors.</p><p>to search for the best filter(s) for the given graph, such as lowpass, band-pass, and signal-rescaling filters. Moreover, rather than using supervised signals to guide the AutoML process, the optimization of AutoProNE is built upon the recent advancements in self-supervised graph representation learning, that is, AutoProNE adopts self-supervised loss to direct the AutoML optimization. Figure <ref type="figure">1</ref> illustrates the framework of AutoProNE.</p><p>We conduct extensive experiments on eight publicly available datasets. By using both network embedding methods without input features (e.g., DeepWalk) and graph neural networks with node features (e.g., DGI), we show that the AutoProNE framework can consistently and significantly enhance the expressive power of graph representations learned by these base methods. For example, the simple, automated, and unsupervised AutoProNE can boost the node classification performance of LINE's representations by 34-44% on the PPI dataset. Furthermore, we show that the graph filters automatically decided by the AutoML process of AutoProNE are always among the best options across all different datasets. Finally, we find that AutoProNE requires only 2-4% of the running time of DeepWalk to offer outperformance by up to 8%, and also demonstrate that its scalability is linear to the number of nodes in the graph, enabling it for handling large-scale data. The code is available at https://github.com/THINK2TRY/AutoProNE. and CogDL 1 <ref type="bibr" target="#b16">[17]</ref> , a open source graph learning library, to make it more convenient to collaborate with existing graph representation algorithms.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head>Contribution. The main contributions of this work include:</head><p>• We investigate the role of graph filters on unsupervised graph representation learning and provide insights into various graph filters. </p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="2">PRELIMINARIES</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="2.1">Concepts</head><p>Graph Notations. Let G=(V, E, X) denote an undirected graph with V as the set of its n nodes and E as its edges, and X ∈ R n×d as the feature matrix of V. Given G, we have its (symmetric) adjacency matrix as A = (a ij ) with a ij = 1 if and only if there exists an edge between v i and v j , as well as its degree matrix</p><formula xml:id="formula_0">D = diag(d 1 , d 2 , ..., d n ) with d i = j a ij .</formula><p>In practice, the row-normalized adjacency matrix Ârw = D −1 A and symmetric normalized adjacency matrix Âsym = D −1/2 AD −1/2 are more commonly used. In this work, we simplify Ârw and Âsym as Â.</p><p>Network Embedding. The problem of network embedding aims to learn a mapping function f : V → R d that projects each node to a d-dimensional space (d |V|). Network embedding methods mainly focus on neighborhood similarity and capture the structural properties of the network. Extensive studies have shown that the learned node representations can benefit various graph mining tasks, such as node classification and link prediction. DeepWalk, LINE, Node2Vec and NetMF are all network embedding methods.</p><p>Graph Signal Processing. In this part, we introduce a recent formulation <ref type="bibr" target="#b17">[18]</ref> of graph signal processing <ref type="bibr" target="#b18">[19]</ref>, <ref type="bibr" target="#b19">[20]</ref> on irregular graphs. The Laplacian matrix of graph G is defined as L = D−A. L = I n − Â is the augmented normalized Laplacian. A vector x ∈ R n defined on the nodes of G is called a graph signal. A useful property of graph Laplacian L is that its quadratic form measures the smoothness of the graph signal. It is easy to verify that</p><formula xml:id="formula_1">x T Lx = i,j A ij (x i − x j ) 2 = (i,j)∈E (x i − x j ) 2<label>(1)</label></formula><p>Let U ∈ R n×n = [u 1 , ..., u n ] T be the eigenvectors of L and we have L = UΛU T , where Λ = diag[λ 1 , ..., λ n ] is the eigenvalues of L corresponding to U. The graph Fourier transform F : R n → R n is defined by Fx = x = U T x, and the inverse graph Fourier transform</p><formula xml:id="formula_2">F −1 is F −1 x = x = U x because FF −1 = U T U = I n .</formula><p>Graph filter is defined based on the graph Fourier transform. Let g: R → R be a function mapping x g −→ y. In frequency domain, the graph filter specified by g is defined by the relation:</p><formula xml:id="formula_3">ỹ = g(Λ) x, that is, ỹ(λ i ) = g(λ i )x(λ i ).</formula><p>In the spatial domain, the above equation is equivalent to y = g( L)x.</p><p>For multi-dimensional cases, the graph Fourier transform is FX = X = U T X and the inverse form is</p><formula xml:id="formula_4">F −1 X = X = U X.</formula><p>Then the graph filter is represented as</p><formula xml:id="formula_5">Y = g( L)X = Ug(Λ)U T X<label>(2)</label></formula><p>Generally, for computational efficiency, Taylor or Chebyshev approximation is applied to avoid the eigendecomposition of L. Without loss of generality, let T ∈ R n×n be the transition matrix and θ i be the weight coefficients. The k-order expansion is represented as</p><formula xml:id="formula_6">g( L) ≈ k i=0 θ i T i ∈ R n×n<label>(3)</label></formula><p>Graph Convolution. In spectral graph convolution networks, the graph convolution operation is fast approximated with the layerwise propagation rule <ref type="bibr" target="#b0">[1]</ref>. GCN simplifies Eq 3 by only keeping the first two items with θ 0 = θ 1 :</p><formula xml:id="formula_7">g( L) = θ 0 I n + θ 1 Â = θ(I n + Â)<label>(4)</label></formula><p>I n is an identity matrix. The eigenvalues of I + Â is in the range [0, 2]. To alleviate the problem of numerical instability and exploding/vanishing gradients when used in deep neural networks, the following renormalization trick is introduced:</p><formula xml:id="formula_8">I n + Â → D−1/2 (I + A) D−1/2 = D−1/2 Ã D−1/2</formula><p>where Dii = j Ãij . Furthermore, multiple layers are stacked to recover a rich class of convolutional filter functions and each layer is followed by a linear transformation and a point-wise non-linearity. Then the one-layer graph convolution becomes as follows:</p><formula xml:id="formula_9">H (i+1) = σ( ÃH (i) Θ (i) )<label>(5)</label></formula><p>where Θ (i) is a layer-specific trainable matrix, H (i) ∈ R n×d is the d-dimensional hidden node representation in the i th layer.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="2.2">ProNE</head><p>In this part, we give a brief introduction to ProNE. ProNE is a fast network embedding method based on matrix factorization. First, it formulates network embedding as a sparse matrix factorization for efficient representation transformation. Second, it utilizes a Gaussian graph filter for representation smoothing to improve the representation.</p><p>Network Embedding as Sparse Matrix Factorization ProNE leverages an edge to represent a node-context pair. Let r i , c i ∈ R d be the node embedding and context vectors of node v i respectively. The concurrence of context v j given v i is</p><formula xml:id="formula_10">pi,j = σ(r T i c j )<label>(6)</label></formula><p>σ() is the sigmoid function. To maximize the concurrence probability and avoid trivial solution (r i = c i &amp;p i,j = 1) for each pair, the objective can be expressed as the weighted sum of log loss over all edges accompanied with negative sampling</p><formula xml:id="formula_11">Loss = − (i,j)∈E [p i,j ln σ(r T i c j ) + τ P E,j ln σ(σ(−r T i c j ))]<label>(7</label></formula><p>) where p i,j = A i,j /D i,i indicates the weight of pair (v i , v j ), τ is the ratio negative sampling, P E,j ∝ ( i:(i,j)∈E p(i, j)) α with α = 1 or 0.75. To minimize the objective equals to let the the partial derivative with respect to r T i c j be zero. And hence we get r T i c j = ln p i,j − ln(τ P E,j )</p><p>ProNE proposes to define a proximity matrix M with each entry as r T i c j , which represents the similarity between embedding of v i and context embedding of v j .</p><formula xml:id="formula_13">M = ln p i,j − ln(τ P E,j ), (v i , v j ) ∈ E 0, (v i , v j ) / ∈ E</formula><p>Now that the relationship matrix is built, the objective is transformed into matrix factorization. ProNE uses a fast randomized tSVD to achieve fast sparse matrix factorization and finally gets X ∈ R N ×d as node embedding matrix.</p><p>Spectral Propagation To address the representation smoothing problem, ProNE proposes to leverage a Gaussian graph filter as the smoothing function f ( Â). ProNE designs the graph filter as</p><formula xml:id="formula_14">g(λ) = e −[ 1 2 (λ−µ) 2 −1]</formula><p>θ and formulates the transformation as the following rule:</p><formula xml:id="formula_15">f ( Â) = D −1 Â(I n − L)<label>(9)</label></formula><p>where I n is the identity matrix and L is defined as the Laplacian filter as:</p><formula xml:id="formula_16">L = Udiag([g(λ 1 ), ..., g(λ n )])U T<label>(10)</label></formula><p>Eq 9 can be viewed as two steps. It first modulates the spectral property with modulator I n − L and then re-propagates information between neighbors.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3">AUTOMATED UNSUPERVISED GRAPH REPRE-SENTATION LEARNING</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.1">Problem</head><p>One GCN layer consists of three steps: neighborhood feature aggregation, feature transformation,and nonlinear transition. By stacking multiple layers, GCNs enable the propagation to reach high-order neighbors. Recently, Wu et al. <ref type="bibr" target="#b14">[15]</ref> suggest that the non-linearity between GCN layers is not critical and thus propose the simplified graph convolution network (SGC) by removing nonlinearity and having only one step of feature propagation and transformation, i.e.,</p><formula xml:id="formula_17">H SGC = ÂK XΘ 1 • • • Θ K = ÂK XΘ<label>(11)</label></formula><p>Inspired by SGC, we can further abstract graph convolution as:</p><formula xml:id="formula_18">H = ÂXΘ = f ( Â)h(X, Θ)<label>(12)</label></formula><p>where f ( Â) and h(X, Θ) are two independent steps for feature representation learning. To make Eq. ( <ref type="formula" target="#formula_18">12</ref>) generalize to unsupervised graph embedding methods, such as DeepWalk and node2vec, we have h(•) as h(A, X, Θ). In these methods, the input feature matrix X is empty and the node representations are learned only based on the graph topology A. Therefore we can have</p><formula xml:id="formula_19">H = f ( Â)h(A, X, Θ)<label>(13)</label></formula><p>In other words, graph representation learning, including both GNNs and unsupervised methods, can be simplified and abstracted as two independent processes: representation transformation h(A, X, Θ) and propagation (or smoothing) f ( Â).</p><p>In representation transformation X = h(A, X, Θ), the node representations X are either learned solely from graph structures without input features X (such as by DeepWalk or NetMF) or transformed with X by learnable parameters (such as MLP or GNNs).</p><p>In the representation smoothing f ( Â) step, the representations initialized in the previous step are propagated to (high-order) neighbors. Note that in traditional unsupervised methods, this step is ignored. In SGC, the features are smoothed via the high order propagation, that is, ÂK .</p><p>Problem. The focus of this work is on the smoothing step of graph representation learning. Specifically, given the node representations of one graph dataset learned by existing methods, such as DeepWalk, the goal is to automatically design a smoothing function f ( Â) for this graph to effectively propagate them over its specific structure in an unsupervised manner.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.2">The AutoProNE Framework</head><p>Inspired by ProNE, we propose that graph signal processing can be a general and powerful method to address the representation smoothing problem. Graph filters, such as the low-pass filter and band-pass filter in the frequency domain, or adjusting the structure importance of nodes in the spatial domain can be used to design the smoothing function f ( Â).</p><p>ProNE uses a fixed Gaussian filter to tackle all cases. However, intuitively, each dataset may require unique graph filters to help "pass" true features and "filter out" noises. However, the input dataset is often considered as a black box and thus it is computationally expensive to analyze its spatial and spectral features. Therefore, it is infeasible to manually select or design appropriate graph filters for each given graph dataset.</p><p>In light of these challenges, we propose the automated Auto-ProNE graph representation learning framework to automatically select graph filters in an unsupervised manner for different input graphs. In parameter selection, the parameter controller automatically selects graph filters from the designated graph filter set together with their hyper-parameters (Cf next section for details). We employ AutoML to implement this process. Briefly, AutoML is designed to automatically build machine learning applications <ref type="bibr" target="#b20">[21]</ref>. It involves two parts-model generation and model evaluation.</p><p>First, model generation can be divided into search space and optimization methods, which are usually classified into hyperparameter optimization (HPO) and architecture optimization (AO). In AutoProNE, we mainly focus on AO, which indicates the model-related parameters, e.g., the selection of graph filters.</p><p>Second, for model evaluation, indicators like accuracy on the validation set are often used as measures. However, our problem is formalized under the unsupervised setting, that is, there exist no supervised indicators to help select the model parameters. To address this issue, we leverage the idea of contrastive learning to maximize the mutual information of different embeddings to evaluate the model.</p><p>In propagation, the node representations X are propagated with selected filters. Under the hypothesis that each graph filter would differently amplify true features and attenuate noises, we concatenate the results of each filter together to preserve the information instead of averaging them, if multiple filters are selected. In order to keep the embedding dimension the same as the input, it is then followed by the SVD operation on the concatenated representations.</p><p>Finally, the loss is collected to help optimize the search. In AutoProNE, we directly utilize Optuna <ref type="bibr" target="#b21">[22]</ref> as the AutoML framework. As the designed search space is small, the algorithm will converge quickly. Algorithm 1 illustrates the process of AutoProNE described above.</p><p>Note that AutoNE <ref type="bibr" target="#b22">[23]</ref> also combines network embedding (NE) with AutoML and attempts to decide the hyperparameters of a given NE algorithm using meta-learning. Differently, Auto-ProNE aims to obtain the optimal graph filters for further improving the embeddings learned by any existing NE algorithms, instead of searching for hyperparameters to have better NE algorithms. In other words, AutoProNE runs on the embedding results and is not related to the learning process of the NE algorithms.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head>Algorithm 1 The AutoProNE Algorithm</head><p>Input: Normalized adjacency matrix Â; Input embeddings X;</p><p>Search iterations N . Output: Enhanced embeddings H with the same dimension size as X.</p><formula xml:id="formula_20">1: for i = 1 to N do 2:</formula><p>Select filters GF s from {P P R, Heat, Gaussian, SR} for each gf ∈ GF s do 5:</p><formula xml:id="formula_21">H gf = P ropagation( Â, X, gf ) 6:</formula><p>Append H gf into Z Calculate the corresponding loss and optimize parameters. 11: end for</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.3">Automated Graph Filter Selection</head><p>We introduce the design choices of the core components in Auto-ProNE: Search Space Design and Unsupervised Loss Function.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.3.1">Search Space Design.</head><p>In graph signal processing, different graph filters have been designed for modulating graph signals. We adopt three existing simple and efficient graph filters-PPR, Heat kernel, and Gaussian kernel-that have been widely used in graph representation learning <ref type="bibr" target="#b15">[16]</ref>, <ref type="bibr" target="#b23">[24]</ref>, <ref type="bibr" target="#b24">[25]</ref> and also propose a new filter based on signal rescaling. The four graph filters are summarized in Table <ref type="table" target="#tab_1">1</ref>.</p><p>PPR <ref type="bibr" target="#b25">[26]</ref>. Personalized PageRank(PPR) is defined based on random walk with restart and reflects the probability of a random walk starting from a node to another. PPR is defined as π(x) = (1 − α) Âπ(x) + αx, and its closed-form matrix is</p><formula xml:id="formula_22">A p = α(I n − (1 − α) Â).</formula><p>To avoid the high computational cost </p><formula xml:id="formula_23">H = A p X α Heat Kernel H = L h X θ Gaussian Kernel H = L g X µ, θ Signal Rescaling H = A s X -</formula><p>of matrix inversion, we use Taylor expansion to approximate A p , that is,</p><formula xml:id="formula_24">A p ≈ k i=0 θ (i) p Â, where θ (i) p = α(1 − α) i<label>(14)</label></formula><p>Heat Kernel <ref type="bibr" target="#b26">[27]</ref>. The heat kernel is often used in heat condition and diffusion, and represents the evolution of temperature in a region whose boundary is held fixed at a particular temperature. When applied to graphs, Heat kernel is defined as f h (λ) = e −θλ , in which θ is a scaling hyperparameter. We denote f h (Λ) as f h (Λ) = diag(e −θλ1 , . . . , e −θλn ). In fact, heat kernel works as a low-pass filter in the frequency domain and the heat graph filter is defined based on the Laplacian matrix as</p><formula xml:id="formula_25">L h = Uf h (Λ)U T = Udiag(e −θλ1 , ..., e −θλn )U T<label>(15)</label></formula><p>Gaussian Kernel <ref type="bibr" target="#b27">[28]</ref>. Gaussian filter is a widely used band-pass filter in signal processing. Gaussian kernel in graph is defined as</p><formula xml:id="formula_26">f (λ) = e −[ 1 2 (λ−µ) 2 −1]</formula><p>θ with µ and θ as the scaling hyperparameters. Gaussian kernel works as a band-pass filter with different hyperparameters. We have f g (Λ) = diag(e −θ λi , . . . , e −θ λi ) if we denote λi = 1 2 (λ i − µ) 2 − 1. Then the Gaussian graph filter is similar to the heat graph filter:</p><formula xml:id="formula_27">L g = Uf g (Λ)U T = Udiag(e −θ λ1 , ..., e −θ λn )U T<label>(16)</label></formula><p>Signal Rescaling. In addition to the three existing filters, we also propose a signal rescaling filter. The intuition is that structural information plays a central role in networks. An intuitive example is that nodes of a high degree may be more important and influential in a network. To capture this phenomenon, we can attenuate node signals (and perform renormalization) before propagation, that is,</p><formula xml:id="formula_28">A s = Normalize( Âσ(D −1 ))<label>(17)</label></formula><p>where</p><formula xml:id="formula_29">σ(x) = 1 1+e −x .</formula><p>Chebyshev Expansion for Efficiency For both the heat kernel and Gaussian kernel, we utilize the Chebyshev expansion and Bessel function <ref type="bibr" target="#b28">[29]</ref> to avoid explicit eigendecomposition. Chebyshev polynomials of the first kind are defined as</p><formula xml:id="formula_30">T i+1 (x) = 2xT i (x) − T i−1 (x) with T 0 (x) = 1, T 1 (x) = x.</formula><p>Then, the expression of a general graph filter can be expanded as:</p><formula xml:id="formula_31">L ≈ U k i=0 c i (θ)T i ( Λ)U T = k i=0 c i (θ)T i ( L)<label>(18)</label></formula><p>where specifically Λ = Λ, L = L for heat kernel and</p><formula xml:id="formula_32">Λ = 1 2 (Λ−µI) 2 , L = 1 2 ( L−µI) 2</formula><p>for Gaussian kernel. The coefficient c i (θ) can be obtained with the Bessel function:</p><formula xml:id="formula_33">c i (θ) = β π T i (x)e −xθ √ 1 − x 2 dx = β(−) i B i (θ)<label>(19)</label></formula><p>where β=1 if i=0 otherwise β=2 and B i (θ) is the modified Bessel function of the first kind <ref type="bibr" target="#b28">[29]</ref>. Then the truncated expansion of the filter becomes as follows:</p><formula xml:id="formula_34">L ≈ B 0 (θ)T 0 ( L) + 2 k−1 i=1 B i (θ)T i ( L)<label>(20)</label></formula><p>This truncated Chebyshev expansion provides a good approximation for e −λθ with a fast convergence rate.</p><p>Taylor expansion and Chebyshev expansion are common approximation methods. <ref type="bibr" target="#b29">[30]</ref> adopts another local spectral embedding method which utilizes random vectors and Gauss-Seidel iteration to avoid explicit eigendecomposition of the adjacency matrix.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.3.2">Unsupervised Loss Function.</head><p>Different from most AutoML settings where supervised information is used, we aim to guide the AutoML process for graph filter selection in an unsupervised or self-supervised fashion. The goal is to derive supervised signals from the input graph data itself for "supervising" the selection of graph filters.</p><p>An additional principle is that the self-supervised loss function Q f of AutoML in the smoothing phase should be different from the one utilized in getting the representations in the transformation phase. The reason lies in that the representations to be smoothed have already achieved the best loss in the transformation step, and a different Q f can help further improve the node representations.</p><p>In AutoProNE, our strategy for automatic graph filter search is built upon the recent development of self-supervised learning techniques, specifically contrastive learning based methods <ref type="bibr" target="#b10">[11]</ref>, <ref type="bibr" target="#b11">[12]</ref>, <ref type="bibr" target="#b30">[31]</ref>. Note that AutoProNE is generally designed for improving node representations learned by both network embedding methods (e.g., DeepWalk) and GNNs. To accommodate their unique properties, we employ the mutual information maximization and instance discrimination as the loss function for both sets of methods, respectively.</p><p>For unsupervised network embedding methods, such as skipgram or matrix factorization based methods, we use the localglobal mutual information maximization loss proposed in <ref type="bibr" target="#b10">[11]</ref> to guide the search of graph filters for each graph. Let Z be the row-wise shuffling of X. X and Z are both propagated with selected graph filters, with the results as H = P rop( X) and H = P rop( Ẑ) respectively. As H is derived from the propagation based on shuffled features, it is "corrupted" and should be less similar to initial embeddings X. We leverage the mean-readout function to obtain a graph level representation: s = 1 N h∈H h. In such case, H is considered as "positive" samples for s, H as "negative" samples for H is derived from shuffled features. The goal is to maximize the mutual information between node features H and global features s in the mean time minimizing the mutual information between s and negative node features Ĥ. Then the loss is formalized as follows:</p><formula xml:id="formula_35">Q f = − 1 2N ( N i=1 E ( X, Â) [log σ(h T i s)] + N j=1 E ( Z, Â) [log σ(1 − hT j s)])<label>(21)</label></formula><p>For graph convolution based methods, InfoNCE proposed in <ref type="bibr" target="#b13">[14]</ref> is utilized as the optimization target. From the perspective of instance discrimination, the contrastive loss is a function whose value is low when a query q is similar to its positive key k + and dissimilar to all other keys (negative keys). In most cases, contrastive learning is often used in conjunction with data augmentation, but data augmentation in graph is still a open problem. In this paper, we simply take input features and the smoothed result as positive pairs. For each node h i ∈ H, xi ∈ X is the only positive key and all the other xj ∈ X, i = j are negative keys. Therefore, we can have the InfoNCE loss with respect to instance discrimination as:</p><formula xml:id="formula_36">Q f = − N i=1 log exp(h T i xi /τ ) K j=0 exp(h T i xj /τ ) (<label>22</label></formula><formula xml:id="formula_37">)</formula><p>where τ is a temperature hyperparameter.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head>Algorithm 2 Propagation</head><p>Input: Normalized ajacency matrix Â; Initial embedding X; Type of graph filter gf ;</p><formula xml:id="formula_38">Output: Enhanced embedding H 1: Order of Expansion k = 5 2: Laplacian matrix L = I − Â X(0) = X 3: if gf ∈ [Heat kernel, Gaussian] then 4:</formula><p>X(1) = LX 5:</p><formula xml:id="formula_39">H = B(0) X(0) − 2B(1) X<label>(1) 6:</label></formula><p>for i = 2 to k do 7:</p><formula xml:id="formula_40">X(i) = 2 L X(i−1) − X(i−2)</formula><p>8:</p><formula xml:id="formula_41">H = H + (−1) i B(i) X(i) 9:</formula><p>end for 10: else if gf is PPR then for i = 1 to k do 13:</p><formula xml:id="formula_42">X(i) = (1 − α) Â X(i−1)</formula><p>14: </p><formula xml:id="formula_43">H = H + X(i)</formula><formula xml:id="formula_44">H = N ormalize( Âσ(D −1 ))X 18: end if 19: return H</formula></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="3.3.3">Automatic Searching</head><p>Now that search space and unsupervised loss functions have been defined, we employ automatic machine learning to search for the best combination of graph filters and hyperparameters. As the loss functions are often non-convex and it is difficult to get the derivative and gradients, hyperparameter optimization in machine learning is generally considered as a problem of blackbox optimization. Bayesian optimization <ref type="bibr" target="#b31">[32]</ref> is a common and powerful method to tackle such cases. The basic idea of Bayesian optimization is to use the Bayesian rule to estimate the posterior distribution of the objective function based on dataset, and then select the next sampling hyperparameter combination according to the distribution. It aims to find the parameters that achieve the most improvement by optimizing the objective function, or loss function. In the implementation, we employ Optuna with Bayesian optimization as the backend AutoML framework for automatic searching. As shown in Algorithm 1, AutoProNE explores better filters and parameters based on previous attempts and losses.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4">ANALYSIS AND DISCUSSIONS</head><p>We provide analyses of the impact of graph filters on the expressiveness of graph representations.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.1">Insight into graph filters</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.1.1">PPR as a low-pass filter</head><p>PPR is defined in the spatial domain. Intuitively, through random walk, a node can capture the information of both direct and distant neighbors. The probability distribution of random walk with restart converges to a stationary distribution:</p><formula xml:id="formula_45">A p = α(I n − (1 − α)AD −1 ) −1 = α(αI n − (1 − α) L) −1 = Udiag( α (1 − α)λ i + α )U T<label>(23)</label></formula><p>In the frequency domain, PPR kernel can be written as f p (λ) = α (1−α)λ+α and is a low-pass filter. This equals to our intuition that random walk usually assigns higher weights to low-order neighbors.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.1.2">Spectral properties of graph filters</head><p>Generally, for the convenience of writing and without loss of generality, we denote a general graph filter matrix with L, where A p , L h and L q are special cases of L. Let λ i be the i th eigenvalue of L, adjacency matrix</p><formula xml:id="formula_46">A = I n − L = I n − Udiag(λ 1 , ..., λ n )U T .</formula><p>GCN in fact works like a low-pass filter from the spectral domain. The propagation of node features by multiplying the (augmented) adjacency matrix Â corresponds to applying graph filter g(λ) = 1 − λ. The eigenvalues of A lie on the interval [0, 2] and it has been proved in <ref type="bibr" target="#b14">[15]</ref> that λ max , the largest eigenvalue of A and λmax , the largest eigenvalue of Â, satisfies:</p><formula xml:id="formula_47">0 &lt; λmax &lt; λ max ≤ 2<label>(24)</label></formula><p>Thus g(λ) = 1 − λ resembles a band-stop filter. The graph filter of GCN can be described as g(λ i ) = (1 − λ i ) K , where K = 1 in one GCN layer and can be any positive integer in Simplified GCN. The spectrum of ÂK actually works as a low- pass-type filter for K &gt; 1 <ref type="bibr" target="#b32">[33]</ref>.</p><p>PPR and Heat kernel work as a low-pass filter. α and θ adjust the pass rate. Gaussian kernel can be generally considered as a band-pass filter. As µ determines the only peak, by adjusting µ and θ, we can implement different types of filter that passes frequencies within a certain range: µ ≤ 0 as low-pass; µ ≥ λmax as high-pass; 0 &lt; µ &lt; λmax as band-pass [28].</p><p>In the spectral domain, the graph filter extracts features in a certain band of the network. Generally, the true features are concentrated in a certain frequency band and the noises conform to uniform or Gaussian distribution. Thus graph filter helps preserve the intrinsic information and reduce the noise. In the spatial domain, the graph filters aggregate the information of both direct and distant neighborhoods into the node embedding. Therefore, the features are properly smoothed and the learned embedding can be more expressive.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.1.3">Spatial Property of SR</head><p>The signal rescaling function is inspired by the fact that many graph convolutional networks are actually performing signal rescaling. In many networks, there exist nodes of very high degrees. For example, the average degree of nodes in BlogCatalog is 32, but the maximum degree is 1,996; DBLP's average node degree is only 2.5, but the maximum degree is also up to 90. The class of most nodes is not determined by its neighbors of a high degree, but neighbors with a lower degree. As a result, attenuating node signals of a high degree helps improve embedding performance in some structure information dominated networks. and Gaussian kernel enlarge the receptive field and assign different weights to neighbors and also pay attention to nonneighbor nodes.They do show different forms when capturing the characteristics of higher-order neighbors. In addition, the three filters assign high weights to the node itself even without adding self-loops. Signal rescaling adjusts weights according to the node degrees of neighbors.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.1.4">Visualization of Graph Filters</head><p>Fig <ref type="figure" target="#fig_4">2</ref> shows the impact of the hyperparameters on filters. And it can be observed that PPR, HeatKernel and Gaussian Kernel are sensitive to hyperparameters, which mainly determine how a node aggregates the features of its neighbors. For PPR, the bigger restart probability α, the more attention a node pays to neighbor nodes. Gaussian and heat kernel are more complex in the spatial domain.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.2">Connection with graph partition</head><p>Graph partition aims to reduce a graph into a set of smaller graphs by partitioning its set of nodes into mutually exclusive groups. In many cases, graphs have good locality and a node often tends to have similar features and be in the same class with its neighbors. The assumption is also the basis of many algorithms like DeepWalk, LINE and GCN. Therefore, the locality and connectivity of a graph are highly related to the effectiveness of the Propagation in our model. Luckily, high-order Cheeger's inequality <ref type="bibr" target="#b33">[34]</ref>, <ref type="bibr" target="#b34">[35]</ref> suggests that eigenvalues of Laplacian matrix are closely associated with a graph's locality and connectivity.</p><p>The effect of graph partition can be measured by graph conductance(a.k.a. Cheeger constant). For a node subset S ⊆ V, the volume of S is vol(S) = x∈S d(x), d(x) is the degree of node x. The edge boundary of S is e(S) = {(x, y) ∈ E|x ∈ S, y / ∈ S}. Then the conductance of S is defined to be:</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head>Φ(S) = |e(S)| min(vol(S), vol( S))</head><p>To measure the conductance of the whole graph G when partitioned into k parts, let S 1 , ..., S k ⊆ V and S i ∩ S j = ∅ if i = j. The k-way Cheeger constant is defined as: ρ G (k) = min{max{Φ(S i ), i = 1, ..., k}} ρ G (k) is positively correlated to graph connectivity. if a graph has higher conductance(bigger ρ G (k)), it is better connected. Highorder Cheeger equality bridges the gap between graph partition and graph spectrum and shows that the eigenvalues of Laplacian matrix control the bounds of k-way Cheeger constant as follows:</p><formula xml:id="formula_48">λ k 2 ≤ ρ G (k) ≤ O(k 2 ) λ k<label>(25)</label></formula><p>In spectral graph theory, the number of connected components in an undirected graph is equal to the multiplicity of the eigenvalue zero in graph Laplacian.   Eq 25 indicates that we can increase(decrease) the graph conductance ρ G (k) by increasing(decreasing) the lower bound λ k . For example, low-pass filters increases λ k for small k and decreases eigenvalues for big k. As a result, different parts become more isolated when the graph is partitioned into different groups, thus improving the locality of the graph and benefiting node classification. In practical applications, different types of graph filters can be selected to fit the characteristics of graphs.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="4.3">Complexity</head><p>The computation of graph filters in Table <ref type="table" target="#tab_1">1</ref> can be efficiently executed in a recurrent manner. Let n = |V|, m = |E|. With Taylor and Chebyshev expansion, we only apply repeated Sparse Matrix-Matrix multiplication (SPMM) between a sparse n × n matrix and a dense n × d feature matrix with time complexity O(md) and avoid explicit eigendecomposition with complexity O(n 3 ). In addition, Intel Math Kernel Library (MKL) provides efficient SPMM operators which can handle graph of millions or even billions of nodes <ref type="bibr" target="#b35">[36]</ref>. This makes it possible for AutoProNE to handle large-scale graph data.</p><p>For Taylor expansion, we denote X(i) = θ i X(i) , X(i) = Â X(i−1) with X(0) = X. For Chebyshev expansion, we denote X(i+1) = c i (θ) X(i) , X(i) = 2 L X(i−1) − X(i−2) with X(0) = X. As L and Â are both sparse matrix, the complexity of Propagation is O(kdm). The dimension reduction (SVD) on small matrix is O(nd 2 ). And the complexity of computing Infomax and InfoNCE loss is also O(nd 2 ) as it only involves the element-wise multiplication of matrix. All together, the complexity of AutoProNE is O(nd 2 + kdm).</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5">EXPERIMENTS</head><p>We conduct extensive experiments to evaluate the effectiveness and efficiency of the proposed AutoProNE framework. Specifically, we examine to what extent AutoProNE can improve both shallow network embedding methods (without input feature matrix) and graph neural networks (with input feature matrix).</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.1">Experiment Setup</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.1.1">Datasets.</head><p>We use eight datasets that are commonly used for evaluating graph representation learning, 6 of which are relatively small scale but are widely used in graph representation learning literature, including BlogCatalog, PPI, Wiki, Cora, Citeseer and Pubmed. DBLP and Youtube are relatively large scale networks. Table <ref type="table" target="#tab_3">2</ref> lists their statistics.</p><p>We use the following five datasets without input node features.</p><p>• BlogCatalog <ref type="bibr" target="#b36">[37]</ref> is a network of social relationships of online bloggers. The vertex labels represent the interests of the bloggers.</p><p>• PPI <ref type="bibr" target="#b37">[38]</ref> is a subgraph of the PPI network for Homo Sapiens.</p><p>The vertex labels are obtained from the hallmark gene sets and represent biological states.</p><p>• DBLP <ref type="bibr" target="#b38">[39]</ref> is an academic citation network where authors are treated as nodes and their dominant conferences as labels.</p><p>• Wiki <ref type="bibr" target="#b39">[40]</ref> is a word co-occurrence network in part of the Wikipedia dump. Node labels are the Part-of-Speech tags.</p><p>• Youtube <ref type="bibr" target="#b36">[37]</ref> is a video-sharing website that allows users to upload, view, rate, share, add to their favorites, report, comment on videos. The labels represent groups of viewers that enjoy common video genres. We consider the following three datasets with input node features.</p><p>• Cora <ref type="bibr" target="#b40">[41]</ref> is a paper citation network. Each publication is associated with a word vector indicating the absence/presence. • Citeseer <ref type="bibr" target="#b40">[41]</ref> is also a paper citation network. Each node has a human-annotated topic as its label and content-based features.</p><p>• Pubmed <ref type="bibr" target="#b41">[42]</ref> contains 19717 diabetes-related publications.</p><p>Each paper in Pubmed is represented by a term frequencyinverse document frequency vector.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.1.2">Baselines</head><p>We compare with several state-of-the-art methods including:</p><p>• DeepWalk <ref type="bibr" target="#b3">[4]</ref> DeepWalk generalizes language model to graph learning. For each vertex, truncated random walks starting from the vertex are used to obtain the contextual information.</p><p>• LINE <ref type="bibr" target="#b4">[5]</ref> LINE preserves the first-order and second-order proximity between vertexes. And we use LINE with the second order proximity. • Node2Vec <ref type="bibr" target="#b5">[6]</ref> Node2vec designs a second order random walk strategy to sample the neighborhood nodes, which interpolates between breadth-first sampling and depth-first sampling.</p><p>• HOPE <ref type="bibr" target="#b6">[7]</ref> HOPE preserves high-order proximities of graphs and capable of capturing the asymmetric transitivity using matrix factorization. • GCN <ref type="bibr" target="#b0">[1]</ref> Graph convolution network (GCN) simplifies graph convolutions by restricting the graph filters to operate in an 1step neighborhood around each node. • GAT <ref type="bibr" target="#b8">[9]</ref> Graph attention networks adopt attention mechanisms to learn the relative weights between two connected nodes. Stacked with the proposed graph filters block, we evaluate how the algorithm performance can be improved.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.1.3">Implementation Details.</head><p>For a fair comparison, we set the dimension of embedding d = 128 for all network embedding methods. For all the other parameters,  we follow the authors' original setup and have the following settings: For DeepWalk, windows size m = 10, #walks per node r = 80, walk length t = 40; For Node2Vec, window size m = 10, #walks per node r = 80, walk length t = 40, p, q are searched over {0.25, 0.50, 1, 2, 4}. For LINE, #negative-samples k = 5 and total sampling budget T = r × t × |V |. For HOPE, β is set to be 0.01. For NetMF, window size r = 5, rank = 256, #negative-samples k = 5. For DeepWalk, LINE and Node2Vec, we use the official code provided by the original authors and for NetMF and HOPE, we use the code implemented in CogDL.</p><p>To further validate the effectiveness of AutoProNE, we also implement AutoProNE on unsupervised convolution-based methods DGI <ref type="bibr" target="#b10">[11]</ref> and unsupervised GraphSAGE <ref type="bibr" target="#b9">[10]</ref>, and compare with semi-supervised GCN <ref type="bibr" target="#b0">[1]</ref> and GAT <ref type="bibr" target="#b8">[9]</ref>. All parameters are set the same as in the authors' original settings. We use the official code provided by the original authors of DGI and unsupervisd GraphSAGE code implemented in CogDL.</p><p>For AutoProNE, each filter can only be selected once. The term number of Taylor and Chebyshev expansion k is set to be 5. For PPR, α is searched between [0.1, 0.9]. For Heat kernel, θ in [0.1, 0.9]. For Gaussian Kernel, µ in [0, 2], θ in [0.2, 1.5].</p><p>Evaluation For non-convolution based methods, we follow the same experimental settings used in baseline works <ref type="bibr" target="#b3">[4]</ref>, <ref type="bibr" target="#b4">[5]</ref>, <ref type="bibr" target="#b5">[6]</ref>, <ref type="bibr" target="#b15">[16]</ref> . We randomly sample different percentages of labeled nodes to train a liblinear classifier and use the remaining for testing. The training ratio for small datasets(PPI, Wiki, BlogCatalog) is 0.1/0.5/0.9, and 0.01/0.05/0.09 for relatively big datasets(DBLP and Youtube). The remaining is for predicting. We repeat the training and predicting 10 times and report the average Micro-F1 for all methods. Analogous results also hold for Macro-F1, which are not shown due to space constraints. For unsupervised convolutional methods, we train a multi-layer perception with a fixed train/valid/test data splitting the same as in <ref type="bibr" target="#b40">[41]</ref>. We repeat it 50 times and report the average accuracy for all methods.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.2">Results</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.2.1">Overall Performance.</head><p>Tables 3 lists the node classification performance based on the embeddings learned by different network embedding algorithms with and without AutoProNE. We test different ratios (0.1, 0.5, 0.9) of labeled data for node classification following existing work <ref type="bibr" target="#b3">[4]</ref>, <ref type="bibr" target="#b4">[5]</ref>, <ref type="bibr" target="#b5">[6]</ref> to train a liblinear classifier and repeat the training and predicting for ten times and report the average Micro-F1 for all methods.</p><p>We observe that the performance of all the base algorithms can be significantly improved by the AutoProNE framework and also the improvements are statistically significant. For DeepWalk, LINE, node2vec, NetMF, and HOPE, the improvements brought by AutoProNE are up to 14.3%, 44.5%, 17%, 6.5%, and 10.9%, respectively. On average, LINE benefits more from AutoProNE as it is in nature an embedding method without incorporating highorder structural information.</p><p>Table <ref type="table" target="#tab_6">4</ref> reports the results of unsupervised GraphSAGE and DGI as well as the AutoProNE version of them. As a reference point, we also list the performance of two popular semi-supervised GNNs-GCN and GAT. We observe that the unsupervised Auto-ProNE framework can help improve the performance of both DGI and GraphSAGE in most cases. This suggests that by automated usage of graph filters, the simple AutoProNE strategy is capable of enhancing graph representation learning with or without input node features. With the help of AutoProNE, DGI can even yield better performance than the end-to-end semi-supervised GCN and GAT models on Pubmed. Finally, we observe that the AutoProNE prefers the newly proposed signal rescaling (SR) filter for BlogCatalog, PPI, Wiki, DBLP and Youtube, while it tends to favor Gaussian kernel for Cora, Citeseer, and Pubmed. We leave the reason behind this difference for future work.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.2.2">The Role of AutoML.</head><p>Tables <ref type="table" target="#tab_8">5 and 6</ref> report the performance of base methods with each of the four graph filters in AutoProNE's search space. We   can observe that different filters have unique impacts on the performance across datasets. For example, Signal Rescaling(SR) and PPR perform relatively better than other filters in dataset PPI, BlogCatalog and Wiki, but for Cora, Citeseer and Pubmed, Gaussian filter exhibits better performance. And the tables show that the performance of AutoProNE is equal to the best result of one single filter, which may imply that AutoProNE finally picks this filter, or our model yields better performance than any single filter, which means AutoProNE learns a better combination of graph filters. These all suggest the need for AutoML to select the best filter(s) for each dataset. The proposed AutoProNE strategy consistently and automatically picks the optimal filter(s) and parameters in an unsupervised manner.</p><p>The graph filter used for the embedding smoothing in ProNE <ref type="bibr" target="#b15">[16]</ref> is a modified 2nd-order Gaussian kernel. For simplicity, the 1st-order Gaussian kernel is covered in AutoProNE's search space. Table <ref type="table" target="#tab_9">7</ref> reports the performance for ProNE(SMF) enhanced by ProNE graph filter and AutoProNE respectively. We can see that the automated search strategy empowers AutoProNE to generate better performance than ProNE in most cases, further demonstrating the effectiveness of using AutoML for smoothing graph representations.</p><p>From the experiment results of AutoML searching, we also have some interesting findings. PPR, Heat kernel and Gaussian kernel perform better if high-order neighbor information matters such as Cora, because SR only aggregates 1st-order neighbors. Besides, low-order methods(like LINE) may benefit more because the original embeddings fail to incorporate abundant neighborhood information.   </p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="5.2.3">Efficiency and Scalability.</head><p>We follow the common practice for efficiency evaluation by the wall-clock time and AutoProNE 's scalability is analyzed by the time cost in multiple-scale networks <ref type="bibr" target="#b4">[5]</ref>. Tables <ref type="table" target="#tab_11">8 and 9</ref> report the extra running time (seconds) when stacked with AutoProNE for 100 searching iterations in 10 threads. Note that AutoProNE is a dataset specific and base agnostic framework. The percentage of extra running time in terms of DeepWalk and DGI is also reported inside the brackets, respectively.</p><p>We can observe that AutoProNE is very efficient compared to base methods. Overall, AutoProNE costs only 2.3-4.7% of DeepWalk's or DGI's running time. Take the Youtube graph as an example, it takes DeepWalk 68,272 seconds (∼19 hours) for generating the embeddings of its 1,000,000+ nodes. However, Auto-ProNE only needs 4.7% of its time to offer 2.6-7.9% performance improvements (Cf. Table <ref type="table" target="#tab_5">3</ref>). For convolutional methods, GNNs are usually less efficient for large scale datasets. This suggests that AutoProNE will take less of the additional percentage of time to achieve improvement.</p><p>We use synthetic networks to demonstrate the scalability of AutoProNE. We generate random regular graphs with a fixed node degree as 10 and the number of nodes ranging between 1,000 and 10,000,000. In addition, we also add the running time on each dataset with the heat kernel and the corresponding loss.</p><p>AutoProNE is ideal for parallel implementation. The computation of our model is mainly spent on iteratively selecting different filters and hyperparameters to evaluate the effectiveness. Therefore, running multi-progresses will speed up the searching of AutoML and achieves great efficiency.</p><p>Table <ref type="table" target="#tab_10">8</ref> shows that ProNE(SMF) is a fast network embedding method. With ProNE(SMF) as the base embedding method, Auto-ProNE works as a general network embedding method with high efficiency and also achieves comparable performance, as shown in Table <ref type="table" target="#tab_9">7</ref>.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="6">RELATED WORK</head></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="6.1">Network Embedding</head><p>Network embedding has been extensively studied by machine learning communities in the past few years and aims to train low dimension vectors that are available for a wide range of downstream tasks.</p><p>The recent emergency of network embedding research begins when skip-gram model <ref type="bibr" target="#b42">[43]</ref>, <ref type="bibr" target="#b43">[44]</ref>, which is originally used in word representation learning and network mining, is applied to derive the embedding of nodes in networks. DeepWalk <ref type="bibr" target="#b3">[4]</ref> and Node2Vec <ref type="bibr" target="#b5">[6]</ref> employ random walks to explore the network structure and LINE <ref type="bibr" target="#b4">[5]</ref> takes a similar idea with an explicit objective function by setting the walk length as one. These random walk based methods can be understood as implicit matrix factorization <ref type="bibr" target="#b7">[8]</ref>.</p><p>The other explicit matrix factorization based network embedding methods have also been proposed. GraRep <ref type="bibr" target="#b44">[45]</ref> directly factorizes different k-order proximity matrices and HOPE <ref type="bibr" target="#b6">[7]</ref> proposes to use generalized SVD to preserve the asymmetric transitivity in directed networks. <ref type="bibr" target="#b45">[46]</ref> also proposes a framework to unify the aforementioned methods. ProNE <ref type="bibr" target="#b15">[16]</ref> formalizes network embedding as sparse matrix factorization and preserves the distributional similarity. ProNE enhances the result of sparse matrix factorization with spectral propagation, which modulates the adjacency matrix mainly to incorporate the global properties in the spatial domain. AutoProNE generalizes the operation to be stacked with existing unsupervised representation learning algorithms in an automated way and improves their performance.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="6.2">Graph Convolution Networks</head><p>Recently semi-supervised graph learning with graph neural networks, such as graph convolution networks (GCNs) <ref type="bibr" target="#b0">[1]</ref>, <ref type="bibr" target="#b46">[47]</ref>, <ref type="bibr" target="#b47">[48]</ref>, draws considerable attention. Various variants <ref type="bibr" target="#b48">[49]</ref>, <ref type="bibr" target="#b49">[50]</ref>, have also been designed to boost the performance. In GCNs, the convolution operation is defined in the spectral space and parametric filters are learned via back-propagation. <ref type="bibr" target="#b23">[24]</ref>, <ref type="bibr" target="#b50">[51]</ref>, <ref type="bibr" target="#b51">[52]</ref>, <ref type="bibr" target="#b52">[53]</ref> replace the adjacency matrix in GCNs with graph filters (PPR and Heat kernel), which they called graph diffusion matrix, to combine the strengths of both spatial and spectral methods and the performance improves. They apply graph filters to semisupervised learning in which graph filters are entangled with the model's training process. AutoProNE proposes a more flexible combination of graph filters in both spectral and spatial domains, which can filter the frequency in any specific band and better extract the intrinsic information and is model-agnostic. Besides, self-supervised learning <ref type="bibr" target="#b53">[54]</ref> is emerging recently and contrastive learning shows great potential. Contrastive methods may employ a scoring function to evaluate the similarity of pairs of data. <ref type="bibr" target="#b13">[14]</ref>, <ref type="bibr" target="#b54">[55]</ref> employ InfoNCE to maximize the gap between positive and negative pairs. One possible intuition behind this is that InfoNCE can shorten the distance between positive pairs, and make the distance between negative pairs as far as possible. <ref type="bibr" target="#b12">[13]</ref> is based on classifying local-global pairs and negative-sampled pairs. And the ultimate goal is to maximize the local-global mutual information. <ref type="bibr" target="#b10">[11]</ref>, <ref type="bibr" target="#b55">[56]</ref>, <ref type="bibr" target="#b56">[57]</ref>, <ref type="bibr" target="#b57">[58]</ref>, <ref type="bibr" target="#b58">[59]</ref>, <ref type="bibr" target="#b59">[60]</ref> apply contrastive methods in graph representation learning and achieves promising results. <ref type="bibr" target="#b55">[56]</ref> contrasts the diffusion result of two graph filters, which also indicates that different filters captures different views of the graph. <ref type="bibr" target="#b11">[12]</ref> employs contrastive coding to pre-train graph neural networks. AutoProNE also maximizes InfoNCE and localglobal mutual information in AutoML loss for optimization.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="6.3">Automated Machine Learning</head><p>With the arising of AutoML <ref type="bibr" target="#b60">[61]</ref>, <ref type="bibr" target="#b61">[62]</ref>, several works also apply it in graph representation learning. GraphNAS <ref type="bibr" target="#b62">[63]</ref> and AutoGNN <ref type="bibr" target="#b63">[64]</ref> aim to generate neural architectures of GNNs in spatial domain with recurrent neural network generator by using reinforcement learning with neural architecture search <ref type="bibr" target="#b64">[65]</ref>. Both of them suffer from high computation costs to find the best model architecture for a given dataset. AutoProNE is more like a plug-and-play framework that can be applied to any graph node embeddings efficiently. Besides, Bayesian optimization <ref type="bibr" target="#b31">[32]</ref>, with the Gaussian process <ref type="bibr" target="#b65">[66]</ref> as the underlying surrogate model, is a popular technique for finding the globally optimal solution of an optimization problem. And this technique is widely used especially in hyperparameter optimization. As AutoProNE mainly aims to search for the best hyperparameters for graph filters, Bayesian Optimization is the principle behind the searching. AutoProNE is an unsupervised and task-independent model that aims to pre-train general embeddings.</p></div>
<div xmlns="http://www.tei-c.org/ns/1.0"><head n="7">CONCLUSION</head><p>In this paper, we investigate the role of graph filters and propose an automated and unsupervised framework AutoProNE to generate improved graph embeddings for unsupervised graph representation learning. AutoProNE comprises four graph filters(PPR, HeatKernel, Gaussian Kernel and Signal Rescaling) and automatically searches for a combination of graph filters and corresponding hyperparameters for the given dataset. Specifically, AutoProNE operates on the adjacency matrix to enrich the context information of each node. It is a flexible and adaptive framework, as the graph filter set can simulate many kinds of filtering functions. It's also very efficient and costs only a little extra time to obtain the improvement in performance.</p><p>The developed method is model-agnostic and can be easily stacked with all unsupervised graph representation learning methods such as DeepWalk, LINE, node2vec, NetMF, and HOPE. On eight publicly available datasets, AutoProNE helps significantly improve the performance of various algorithms. In addition, AutoProNE can also enhance the performance of selfsupervised/unsupervised GNN methods, e.g., DGI and Graph-Sage. We show that the self-supervised DGI model with the unsupervised AutoProNE can generate comparable or even better performance than semi-supervised end-to-end GNN methods, such as GCN and GAT. We have implemented AutoProNE in CogDL, an open-source graph learning library, to help more graph representation learning methods.</p></div><figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_0"><head></head><label></label><figDesc>Fig 1 shows the overall architecture of AutoProNE, which first utilizes the idea of AutoML to select suitable graph filters for modulating graph signals (parameter selection) and then smooth node representations based on the selected filters (propagation).</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_1"><head>3 :</head><label>3</label><figDesc>Let Z be an empty list: Z = [] 4:</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_2"><head>8 : 9 :</head><label>89</label><figDesc>Concatenate smoothed embeddings in Z to have Z rConduct dimension reduction on Z r to get H 10:</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_4"><head>Fig 2</head><label>2</label><figDesc>exhibits the visualization results of the functions of different filters on Karate Clubs dataset. Compared to merely row normalization, as we can see from the figures, PPR, HeatKernel</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_5"><head></head><label></label><figDesc>A P with α = 0.2 (d) A P with α = 0.8 (e) L h with θ = 0.2 (f) L h with θ = 0.2 (g) Lg with µ = 0.2 and θ = 1.0 (h) Lg with µ = −1 and θ = 2</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_6"><head>Fig. 2 .</head><label>2</label><figDesc>Fig. 2. Visualization of adjacency matrix A, row normalized adjacency matrix with self-loops Ârw, PPR matrix A P , Gaussian filter matrix Lg, Heat kernel filter matrix L h and signal rescaling matrix Ar on dataset Karate Clubs. The darker the color means the higher the weight of the node. The weight is between [0, 1].</figDesc><graphic url="image-13.png" coords="7,333.13,527.42,92.22,91.98" type="bitmap" /></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_8"><head></head><label></label><figDesc>Different loss function.</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" xml:id="fig_9"><head>Fig. 3 .</head><label>3</label><figDesc>Fig. 3. AutoProNE's Scalability w.r.t. network volume. Running time as #node grows with node degree fixed to 10. As the network size increases, the time cost of both graph filters and computing loss also grows linearly.</figDesc></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_1"><head>TABLE 1</head><label>1</label><figDesc></figDesc><table><row><cell></cell><cell>Graph Filters</cell></row><row><cell>Name</cell><cell>Graph Filter Parameters</cell></row><row><cell>PPR</cell><cell></cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_3"><head>TABLE 2</head><label>2</label><figDesc>Statistics of datasets.</figDesc><table><row><cell>Dataset</cell><cell>Nodes</cell><cell cols="4">Edges Classes Features Degree</cell></row><row><cell>BlogCatalog</cell><cell>10,312</cell><cell>333,983</cell><cell>39</cell><cell>-</cell><cell>32.4</cell></row><row><cell>PPI</cell><cell>3,890</cell><cell>76,584</cell><cell>50</cell><cell>-</cell><cell>19.7</cell></row><row><cell>Wiki</cell><cell>4,777</cell><cell>184,812</cell><cell>40</cell><cell>-</cell><cell>38.7</cell></row><row><cell>DBLP</cell><cell>51,264</cell><cell>127,968</cell><cell>60</cell><cell>-</cell><cell>2.5</cell></row><row><cell>Youtube</cell><cell cols="2">1,138,499 2,990,443</cell><cell>47</cell><cell>-</cell><cell>2.6</cell></row><row><cell>Cora</cell><cell>2,708</cell><cell>5,429</cell><cell>7</cell><cell>1,433</cell><cell>2.0</cell></row><row><cell>Citeseer</cell><cell>3,327</cell><cell>4,732</cell><cell>6</cell><cell>3,703</cell><cell>1.4</cell></row><row><cell>Pubmed</cell><cell>19,717</cell><cell>44,338</cell><cell>3</cell><cell>500</cell><cell>2.2</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_5"><head>TABLE 3</head><label>3</label><figDesc>Micro-F1 results of node classification by different algorithms w/ and w/o AutoProNE. Ratio indicates the percentage of labeled data.Numbers in the brackets indicate performance improvements and all are statistically significant (p-value 0.01; t-test).</figDesc><table><row><cell>Datasets</cell><cell cols="3">Ratio DeepWalk ProDeepWalk</cell><cell>LINE ProLINE</cell><cell cols="2">node2vec ProNode2vec</cell><cell cols="2">NetMF ProNetMF</cell><cell cols="2">HOPE ProHOPE</cell></row><row><cell></cell><cell>0.1</cell><cell>35.6</cell><cell>36.2 (+1.7%)</cell><cell>30.3 32.3 (+6.6%)</cell><cell>35.7</cell><cell>35.7 (0.0%)</cell><cell>35.6</cell><cell>36.8 (+3.4%)</cell><cell>30.4</cell><cell>33.5 (+10.2%)</cell></row><row><cell>BlogCatalog</cell><cell>0.5</cell><cell>40.5</cell><cell>41.8 (+3.2%)</cell><cell>37.1 38.3 (+3.2%)</cell><cell>40.6</cell><cell>41.5 (+2.2%)</cell><cell>41.1</cell><cell>41.9 (+2.0%)</cell><cell>34.0</cell><cell>37.4 (+10.0%)</cell></row><row><cell></cell><cell>0.9</cell><cell>42.3</cell><cell>44.2 (+4.5%)</cell><cell>39.6 40.5 (+2.3%)</cell><cell>41.8</cell><cell>43.9 (+5.0%)</cell><cell>41.6</cell><cell>42.3 (+1.7%)</cell><cell>35.3</cell><cell>38.3 (+8.5%)</cell></row><row><cell></cell><cell>0.1</cell><cell>16.7</cell><cell>17.6 (+5.4%)</cell><cell>12.5 17.0 (+34.9%)</cell><cell>16.1</cell><cell>17.5 (+8.7%)</cell><cell>17.9</cell><cell>18.0 (+0.6%)</cell><cell>16.0</cell><cell>17.3 (+8.1%)</cell></row><row><cell>PPI</cell><cell>0.5</cell><cell>21.6</cell><cell>24.7 (+14.3%)</cell><cell>16.4 23.7 (+44.5%)</cell><cell>20.6</cell><cell>24.1 (+17.0%)</cell><cell>23.1</cell><cell>24.6 (+6.5%)</cell><cell>21.0</cell><cell>23.3 (+10.9%)</cell></row><row><cell></cell><cell>0.9</cell><cell>24.0</cell><cell>27.0 (+12.5%)</cell><cell>19.5 26.2 (+34.4%)</cell><cell>23.1</cell><cell>25.7 (+11.2%)</cell><cell>25.5</cell><cell>26.5 (+3.9%)</cell><cell>23.2</cell><cell>24.9 (+7.3%)</cell></row><row><cell></cell><cell>0.1</cell><cell>43.3</cell><cell>44.5 (+2.8%)</cell><cell>41.8 45.8 (+9.6%)</cell><cell>44.8</cell><cell>44.2 (-1.3%)</cell><cell>45.7</cell><cell>45.9 (+0.5%)</cell><cell>48.8</cell><cell>48.0 (+2.4%)</cell></row><row><cell>Wiki</cell><cell>0.5</cell><cell>49.2</cell><cell>50.0 (+1.6%)</cell><cell>52.5 53.2 (+1.3%)</cell><cell>51.1</cell><cell>50.9 (-0.3%)</cell><cell>50.1</cell><cell>50.9 (+1.6%)</cell><cell>53.1</cell><cell>52.8 (-0.5%)</cell></row><row><cell></cell><cell>0.9</cell><cell>50.0</cell><cell>51.4 (+2.8%)</cell><cell>54.7 55.0 (+0.5%)</cell><cell>52.8</cell><cell>52.5 (-0.5%)</cell><cell>50.7</cell><cell>51.9 (+2.4%)</cell><cell>53.1</cell><cell>54.3 (+0.4%)</cell></row><row><cell></cell><cell>0.01</cell><cell>51.5</cell><cell>55.8 (+8.3%)</cell><cell>49.7 52.4 (+5.4%)</cell><cell>53.4</cell><cell>57.8 (+8.2%)</cell><cell>51.5</cell><cell>52.9 (+2.7%)</cell><cell>-</cell><cell>-</cell></row><row><cell>DBLP</cell><cell>0.05</cell><cell>58.1</cell><cell>59.0 (+1.5%)</cell><cell>54.9 56.2 (+2.4%)</cell><cell>58.3</cell><cell>60.0 (+2.9%)</cell><cell>57.1</cell><cell>59.5 (+4.2%)</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>0.09</cell><cell>59.4</cell><cell>59.9 (+0.9%)</cell><cell>56.3 57.0 (+1.2%)</cell><cell>59.5</cell><cell>60.6 (+1.8%)</cell><cell>57.9</cell><cell>60.2 (+4.0%)</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>0.01</cell><cell>38.2</cell><cell>39.2 (+2.6%)</cell><cell>33.2 39.8 (+19.8%)</cell><cell>38.2</cell><cell>39.7 (+3.9%)</cell><cell>-</cell><cell>-</cell><cell>-</cell><cell>-</cell></row><row><cell>Youtube</cell><cell>0.05</cell><cell>41.6</cell><cell>44.7 (+6.0%)</cell><cell>36.2 43.5 (+20.1%)</cell><cell>40.0</cell><cell>45.3 (+12.2%)</cell><cell>-</cell><cell>-</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>0.09</cell><cell>42.8</cell><cell>46.2 (+7.9%)</cell><cell>38.3 45.9 (+19.8%)</cell><cell>43.0</cell><cell>47.1 (+9.5%)</cell><cell>-</cell><cell>-</cell><cell>-</cell><cell>-</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_6"><head>TABLE 4</head><label>4</label><figDesc>Accuracy results of node classification by unsupervised GNNs. Significant test (p-value 0.01; t-test).</figDesc><table><row><cell></cell><cell>Dataset</cell><cell>Cora</cell><cell>Pubmed</cell><cell>Citeseer</cell></row><row><cell>Semi-supervised</cell><cell>GCN GAT</cell><cell cols="3">81.5 83.0 ± 0.7 79.0 ± 0.3 72.5 ± 0.7 79.0 70.3</cell></row><row><cell></cell><cell>DGI</cell><cell cols="3">82.0 ± 0.1 77.1 ± 0.1 71.7 ± 0.2</cell></row><row><cell>Unsupervised</cell><cell cols="4">ProDGI GraphSAGE 77.2 ± 0.1 78.0 ± 0.1 61.2 ± 0.1 82.9 ± 0.2 81.0 ± 0.1 70.8 ± 0.2</cell></row><row><cell></cell><cell>ProSAGE</cell><cell cols="3">78.1 ± 0.2 79.5 ± 0.1 62.1 ± 0.2</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_7"><head>TABLE 5</head><label>5</label><figDesc>Results of base embedding methods with different graph filters.Ratio=0.5 for BlogCatalog, PPI, and Wiki; 0.05 for DBLP and Youtube.</figDesc><table><row><cell>Dataset</cell><cell>Type</cell><cell cols="5">DeepWalk LINE node2vec NetMF HOPE</cell></row><row><cell></cell><cell>Heat</cell><cell>41.4</cell><cell>38.3</cell><cell>41.0</cell><cell>41.6</cell><cell>34.6</cell></row><row><cell>BlogCatalog</cell><cell>PPR</cell><cell>41.7</cell><cell>38.8</cell><cell>41.3</cell><cell>41.8</cell><cell>35.6</cell></row><row><cell></cell><cell>Gaussian</cell><cell>41.4</cell><cell>38.4</cell><cell>41.1</cell><cell>41.3</cell><cell>37.5</cell></row><row><cell></cell><cell>SR</cell><cell>41.9</cell><cell>38.7</cell><cell>40.9</cell><cell>41.6</cell><cell>34.5</cell></row><row><cell></cell><cell>AutoProNE</cell><cell>41.8</cell><cell>38.3</cell><cell>41.5</cell><cell>41.9</cell><cell>37.4</cell></row><row><cell></cell><cell>Heat</cell><cell>23.4</cell><cell>21.1</cell><cell>22.8</cell><cell>24.0</cell><cell>21.7</cell></row><row><cell>PPI</cell><cell>PPR</cell><cell>23.9</cell><cell>22.7</cell><cell>23.6</cell><cell>24.3</cell><cell>22.3</cell></row><row><cell></cell><cell>Gaussian</cell><cell>23.2</cell><cell>21.3</cell><cell>22.8</cell><cell>23.7</cell><cell>21.1</cell></row><row><cell></cell><cell>SR</cell><cell>24.5</cell><cell>23.0</cell><cell>24.8</cell><cell>25.0</cell><cell>23.0</cell></row><row><cell></cell><cell>AutoProNE</cell><cell>24.7</cell><cell>23.7</cell><cell>24.1</cell><cell>24.6</cell><cell>23.3</cell></row><row><cell></cell><cell>Heat</cell><cell>48.2</cell><cell>52.8</cell><cell>50.5</cell><cell>47.4</cell><cell>53.1</cell></row><row><cell>Wiki</cell><cell>PPR</cell><cell>48.4</cell><cell>52.6</cell><cell>49.9</cell><cell>48.1</cell><cell>53.2</cell></row><row><cell></cell><cell>Gaussian</cell><cell>48.2</cell><cell>52.6</cell><cell>50.3</cell><cell>47.2</cell><cell>53.0</cell></row><row><cell></cell><cell>SR</cell><cell>49.0</cell><cell>54.1</cell><cell>52.2</cell><cell>50.7</cell><cell>53.0</cell></row><row><cell></cell><cell>AutoProNE</cell><cell>50.0</cell><cell>53.2</cell><cell>50.9</cell><cell>50.9</cell><cell>52.8</cell></row><row><cell></cell><cell>Heat</cell><cell>58.8</cell><cell>54.7</cell><cell>59.4</cell><cell>58.8</cell><cell>-</cell></row><row><cell>DBLP</cell><cell>PPR</cell><cell>59.0</cell><cell>55.4</cell><cell>59.7</cell><cell>59.0</cell><cell>-</cell></row><row><cell></cell><cell>Gaussian</cell><cell>58.9</cell><cell>54.7</cell><cell>59.7</cell><cell>58.5</cell><cell>-</cell></row><row><cell></cell><cell>SR</cell><cell>58.7</cell><cell>54.1</cell><cell>59.7</cell><cell>58.9</cell><cell>-</cell></row><row><cell></cell><cell>AutoProNE</cell><cell>59.0</cell><cell>56.2</cell><cell>60.0</cell><cell>59.5</cell><cell>-</cell></row><row><cell></cell><cell>Heat</cell><cell>44.5</cell><cell>42.7</cell><cell>44.7</cell><cell>-</cell><cell>-</cell></row><row><cell>Youtube</cell><cell>PPR</cell><cell>44.6</cell><cell>43.5</cell><cell>45.1</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>Gaussian</cell><cell>44.3</cell><cell>40.5</cell><cell>44.3</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>SR</cell><cell>44.5</cell><cell>43.0</cell><cell>45.1</cell><cell>-</cell><cell>-</cell></row><row><cell></cell><cell>AutoProNE</cell><cell>44.7</cell><cell>43.5</cell><cell>45.3</cell><cell>-</cell><cell>-</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_8"><head>TABLE 6</head><label>6</label><figDesc>Results of base GNNs with different graph filters.</figDesc><table><row><cell>Dataset</cell><cell>Type</cell><cell cols="3">Cora Citeseer Pubmed</cell></row><row><cell></cell><cell>Heat</cell><cell>82.0</cell><cell>71.8</cell><cell>77.5</cell></row><row><cell>DGI</cell><cell>PPR</cell><cell>64.2</cell><cell>70,1</cell><cell>77.4</cell></row><row><cell></cell><cell>Gaussian</cell><cell>82.9</cell><cell>71.4</cell><cell>80.7</cell></row><row><cell></cell><cell>SR</cell><cell>13.1</cell><cell>70.1</cell><cell>77.2</cell></row><row><cell></cell><cell cols="2">AutoProNE 82.9</cell><cell>70.8</cell><cell>81.0</cell></row><row><cell></cell><cell>Heat</cell><cell>76.5</cell><cell>61.7</cell><cell>77.4</cell></row><row><cell>GraphSAGE</cell><cell>PPR</cell><cell>62.1</cell><cell>62.0</cell><cell>77.6</cell></row><row><cell></cell><cell>Gaussian</cell><cell>77.8</cell><cell>62.3</cell><cell>76.6</cell></row><row><cell></cell><cell>SR</cell><cell>16.5</cell><cell>62.7</cell><cell>77.1</cell></row><row><cell></cell><cell cols="2">AutoProNE 78.1</cell><cell>62.2</cell><cell>79.5</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_9"><head>TABLE 7</head><label>7</label><figDesc>Results of ProNE and AutoProNE. With ProNE and With AutoProNE mean the result of ProNE(SMF) improved by the graph filter of ProNE and AutoProNE respectively. .8 39.1 15.1 22.0 24.5 47.8 54.5 55.6 46.7 54.0 55.6 36.4 41.4 42.5 With ProNE 36.4 40.9 42.2 17.5 24.0 26.5 48.0 54.6 56.0 46.7 55.2 56.3 37.6 42.9 43.9 With AutoProNE 35.8 41.0 42.2 17.7 24.3 26.5 48.6 55.5 56.8 50.0 56.1 57.5 38.7 43.7 44.6</figDesc><table><row><cell>Method</cell><cell cols="3">BlogCatalog</cell><cell></cell><cell>PPI</cell><cell></cell><cell></cell><cell>Wiki</cell><cell>DBLP</cell><cell>Youtube</cell></row><row><cell>Ratio</cell><cell>0.1</cell><cell>0.5</cell><cell>0.9</cell><cell>0.1</cell><cell>0.5</cell><cell>0.9</cell><cell>0.1</cell><cell>0.5</cell><cell cols="2">0.9 0.01 0.05 0.09 0.01 0.05 0.09</cell></row><row><cell>ProNE(SMF)</cell><cell cols="2">33.0 37</cell><cell></cell><cell></cell><cell></cell><cell></cell><cell></cell><cell></cell><cell></cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_10"><head>TABLE 8</head><label>8</label><figDesc>Efficiency of AutoProNE (seconds). SMF stands for ProNE(SMF).</figDesc><table><row><cell>Dataset</cell><cell cols="6">DeepWalk LINE node2vec SMF NetMF HOPE</cell><cell>AutoProNE</cell></row><row><cell>PPI</cell><cell>272</cell><cell>70</cell><cell>716</cell><cell>2</cell><cell>10</cell><cell>12</cell><cell>+11 (4.0%)</cell></row><row><cell>Wiki</cell><cell>494</cell><cell>87</cell><cell>819</cell><cell>4</cell><cell>23</cell><cell>17</cell><cell>+12 (2.4%)</cell></row><row><cell>BlogCatalog</cell><cell>1,231</cell><cell>185</cell><cell>2,809</cell><cell>12</cell><cell>144</cell><cell>136</cell><cell>+29 (2.3%)</cell></row><row><cell>DBLP</cell><cell cols="2">3,825 1,204</cell><cell>4,749</cell><cell>15</cell><cell>186</cell><cell>-</cell><cell>+100 (2.6%)</cell></row><row><cell>Youtube</cell><cell cols="2">68,272 5,890</cell><cell cols="2">30,218 302</cell><cell>-</cell><cell cols="2">-+3,213 (4.7%)</cell></row></table></figure>
<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_11"><head>TABLE 9</head><label>9</label><figDesc>Efficiency of AutoProNE (seconds).</figDesc><table><row><cell>Dataset</cell><cell cols="2">DGI GraphSAGE</cell><cell>AutoProNE</cell></row><row><cell>Cora</cell><cell>341</cell><cell>118</cell><cell>+15 (4.1%)</cell></row><row><cell>Citeseer</cell><cell>490</cell><cell>131</cell><cell>+21 (4.2%)</cell></row><row><cell cols="2">Pubmed 4,863</cell><cell cols="2">1,254 +183 (3.7%)</cell></row></table></figure>
		</body>
		<back>

			<div type="acknowledgement">
<div xmlns="http://www.tei-c.org/ns/1.0"><head>ACKNOWLEDGMENTS</head><p>The work is supported by the National Key R&amp;D Program of China (2018YFB1402600), NSFC for Distinguished Young Scholar (61825602), and NSFC (61836013).</p></div>
			</div>

			<div type="references">

				<listBibl>

<biblStruct xml:id="b0">
	<analytic>
		<title level="a" type="main">Semi-supervised classification with graph convolutional networks</title>
		<author>
			<persName><forename type="first">T</forename><forename type="middle">N</forename><surname>Kipf</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Welling</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICLR</title>
				<imprint>
			<date type="published" when="2017">2017</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b1">
	<analytic>
		<title level="a" type="main">Graph convolutional neural networks for web-scale recommender systems</title>
		<author>
			<persName><forename type="first">R</forename><surname>Ying</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>He</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Eksombatchai</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><forename type="middle">L</forename><surname>Hamilton</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Leskovec</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2018">2018</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b2">
	<analytic>
		<title level="a" type="main">Cognitive graph for multi-hop reading comprehension at scale</title>
		<author>
			<persName><forename type="first">M</forename><surname>Ding</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Zhou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Yang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ACL</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b3">
	<analytic>
		<title level="a" type="main">Deepwalk: online learning of social representations</title>
		<author>
			<persName><forename type="first">B</forename><surname>Perozzi</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>Al-Rfou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Skiena</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2014">2014</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b4">
	<monogr>
		<title level="m" type="main">Line: Largescale information network embedding</title>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Qu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Yan</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Mei</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2015">2015</date>
			<publisher>WWW</publisher>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b5">
	<analytic>
		<title level="a" type="main">node2vec: Scalable feature learning for networks</title>
		<author>
			<persName><forename type="first">A</forename><surname>Grover</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Leskovec</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b6">
	<analytic>
		<title level="a" type="main">Asymmetric transitivity preserving graph embedding</title>
		<author>
			<persName><forename type="first">M</forename><surname>Ou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Cui</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Pei</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><surname>Zhu</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b7">
	<monogr>
		<title level="m" type="main">Network embedding as matrix factorization: Unifying deepwalk, line, pte, and node2vec</title>
		<author>
			<persName><forename type="first">J</forename><surname>Qiu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Dong</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Ma</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Li</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<editor>WSDM</editor>
		<imprint>
			<date type="published" when="2018">2018</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b8">
	<monogr>
		<title level="m" type="main">Graph attention networks</title>
		<author>
			<persName><forename type="first">P</forename><surname>Velickovic</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Cucurull</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Casanova</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Romero</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Liò</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Bengio</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2018">2018</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b9">
	<analytic>
		<title level="a" type="main">Inductive representation learning on large graphs</title>
		<author>
			<persName><forename type="first">W</forename><surname>Hamilton</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Ying</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Leskovec</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2017">2017</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b10">
	<monogr>
		<title level="m" type="main">Deep graph infomax</title>
		<author>
			<persName><forename type="first">P</forename><surname>Velickovic</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><surname>Fedus</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><forename type="middle">L</forename><surname>Hamilton</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Liò</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Bengio</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><forename type="middle">D</forename><surname>Hjelm</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b11">
	<analytic>
		<title level="a" type="main">Gcc: Graph contrastive coding for graph neural network pretraining</title>
		<author>
			<persName><forename type="first">J</forename><surname>Qiu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Dong</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Yang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Ding</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b12">
	<monogr>
		<title level="m" type="main">Learning deep representations by mutual information estimation and maximization</title>
		<author>
			<persName><forename type="first">R</forename><forename type="middle">H</forename><surname>Devon</surname></persName>
		</author>
		<author>
			<persName><forename type="first">F</forename><surname>Alex</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L.-M</forename><surname>Samuel</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Karan</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Phil</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Adam</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Yoshua</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b13">
	<analytic>
		<title level="a" type="main">Momentum contrast for unsupervised visual representation learning</title>
		<author>
			<persName><forename type="first">K</forename><surname>He</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Fan</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Wu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Xie</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>Girshick</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">CVPR</title>
				<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b14">
	<analytic>
		<title level="a" type="main">Simplifying graph convolutional networks</title>
		<author>
			<persName><forename type="first">F</forename><surname>Wu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><forename type="middle">H S</forename><genName>Jr</genName></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Fifty</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Yu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><forename type="middle">Q</forename><surname>Weinberger</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICML</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b15">
	<analytic>
		<title level="a" type="main">Prone: fast and scalable network representation learning</title>
		<author>
			<persName><forename type="first">J</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Dong</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Ding</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">IJCAI</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b16">
	<monogr>
		<title level="m" type="main">Cogdl: An extensive toolkit for deep learning on graphs</title>
		<author>
			<persName><forename type="first">Y</forename><surname>Cen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Hou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Luo</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Yao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Zeng</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Guo</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Dai</surname></persName>
		</author>
		<idno type="arXiv">arXiv:2103.00959</idno>
		<imprint>
			<date type="published" when="2021">2021</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b17">
	<analytic>
		<title level="a" type="main">Irregularity-aware graph fourier transforms</title>
		<author>
			<persName><forename type="first">B</forename><surname>Girault</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Ortega</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><forename type="middle">S</forename><surname>Narayanan</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">IEEE Transactions on Signal Processing</title>
		<imprint>
			<biblScope unit="volume">66</biblScope>
			<biblScope unit="issue">21</biblScope>
			<biblScope unit="page" from="5746" to="5761" />
			<date type="published" when="2018">2018</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b18">
	<analytic>
		<title level="a" type="main">Discrete signal processing on graphs</title>
		<author>
			<persName><forename type="first">A</forename><surname>Sandryhaila</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><forename type="middle">M</forename><surname>Moura</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">IEEE transactions on signal processing</title>
		<imprint>
			<biblScope unit="volume">61</biblScope>
			<biblScope unit="issue">7</biblScope>
			<biblScope unit="page" from="1644" to="1656" />
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b19">
	<analytic>
		<title level="a" type="main">The emerging field of signal processing on graphs: Extending highdimensional data analysis to networks and other irregular domains</title>
		<author>
			<persName><forename type="first">D</forename><forename type="middle">I</forename><surname>Shuman</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><forename type="middle">K</forename><surname>Narang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Frossard</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Ortega</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Vandergheynst</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">IEEE signal processing magazine</title>
		<imprint>
			<biblScope unit="volume">30</biblScope>
			<biblScope unit="issue">3</biblScope>
			<biblScope unit="page" from="83" to="98" />
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b20">
	<monogr>
		<title level="m" type="main">Automl: A survey of the state-of-the-art</title>
		<author>
			<persName><forename type="first">X</forename><surname>He</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Zhao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Chu</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1908.00709</idno>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b21">
	<analytic>
		<title level="a" type="main">Optuna: A nextgeneration hyperparameter optimization framework</title>
		<author>
			<persName><forename type="first">T</forename><surname>Akiba</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Sano</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Yanase</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Ohta</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Koyama</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b22">
	<analytic>
		<title level="a" type="main">Autone: Hyperparameter optimization for massive network embedding</title>
		<author>
			<persName><forename type="first">K</forename><surname>Tu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Ma</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Cui</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Pei</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><surname>Zhu</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b23">
	<analytic>
		<title level="a" type="main">Diffusion improves graph learning</title>
		<author>
			<persName><forename type="first">J</forename><surname>Klicpera</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Weißenberger</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Günnemann</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2019">2019</date>
			<biblScope unit="volume">13</biblScope>
			<biblScope unit="page">345</biblScope>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b24">
	<analytic>
		<title level="a" type="main">Graph convolutional networks using heat kernel for semi-supervised learning</title>
		<author>
			<persName><forename type="first">B</forename><surname>Xu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Shen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Cao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Cen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Cheng</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">IJCAI</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b25">
	<monogr>
		<title level="m" type="main">The pagerank citation ranking: Bringing order to the web</title>
		<author>
			<persName><forename type="first">L</forename><surname>Page</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Brin</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>Motwani</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Winograd</surname></persName>
		</author>
		<imprint>
			<date type="published" when="1999">1999</date>
			<publisher>Stanford InfoLab, Tech. Rep</publisher>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b26">
	<analytic>
		<title level="a" type="main">Diffusion kernels on graphs and other discrete structures</title>
		<author>
			<persName><forename type="first">R</forename><forename type="middle">I</forename><surname>Kondor</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Lafferty</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICML</title>
				<imprint>
			<date type="published" when="2002">2002</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b27">
	<analytic>
		<title level="a" type="main">Vertex-frequency analysis on graphs</title>
		<author>
			<persName><forename type="first">D</forename><forename type="middle">I</forename><surname>Shuman</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Ricaud</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Vandergheynst</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">Applied and Computational Harmonic Analysis</title>
		<imprint>
			<biblScope unit="volume">40</biblScope>
			<biblScope unit="issue">2</biblScope>
			<biblScope unit="page" from="260" to="291" />
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b28">
	<monogr>
		<title level="m" type="main">Special functions of mathematics for engineers</title>
		<author>
			<persName><forename type="first">L</forename><forename type="middle">C</forename><surname>Andrews</surname></persName>
		</author>
		<imprint>
			<date type="published" when="1998">1998</date>
			<biblScope unit="volume">49</biblScope>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b29">
	<monogr>
		<title level="m" type="main">Graphzoom: A multi-level spectral approach for accurate and scalable graph embedding</title>
		<author>
			<persName><forename type="first">C</forename><surname>Deng</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Zhao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Feng</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b30">
	<monogr>
		<title level="m" type="main">Infograph: Unsupervised and semi-supervised graph-level representation learning via mutual information maximization</title>
		<author>
			<persName><forename type="first">F.-Y</forename><surname>Sun</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Hoffmann</surname></persName>
		</author>
		<author>
			<persName><forename type="first">V</forename><surname>Verma</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b31">
	<analytic>
		<title level="a" type="main">Practical bayesian optimization of machine learning algorithms</title>
		<author>
			<persName><forename type="first">J</forename><surname>Snoek</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Larochelle</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><forename type="middle">P</forename><surname>Adams</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2012">2012</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b32">
	<monogr>
		<title level="m" type="main">Revisiting graph neural networks: All we have is low-pass filters</title>
		<author>
			<persName><forename type="first">H</forename><surname>Nt</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Maehara</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1905.09550</idno>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b33">
	<monogr>
		<title level="m" type="main">Multiway spectral partitioning and higher-order cheeger inequalities</title>
		<author>
			<persName><forename type="first">J</forename><forename type="middle">R</forename><surname>Lee</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><forename type="middle">O</forename><surname>Gharan</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Trevisan</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2014">2014</date>
			<publisher>JACM</publisher>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b34">
	<analytic>
		<title level="a" type="main">A cheeger inequality for the graph connection laplacian</title>
		<author>
			<persName><forename type="first">A</forename><forename type="middle">S</forename><surname>Bandeira</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Singer</surname></persName>
		</author>
		<author>
			<persName><forename type="first">D</forename><forename type="middle">A</forename><surname>Spielman</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">SIAM Journal on Matrix Analysis and Applications</title>
		<imprint>
			<biblScope unit="volume">34</biblScope>
			<biblScope unit="issue">4</biblScope>
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b35">
	<monogr>
		<title level="m" type="main">Lightne: A lightweight graph processing system for network embedding</title>
		<author>
			<persName><forename type="first">J</forename><surname>Qiu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Dhulipala</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>Peng</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Wang</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2021">2021</date>
		</imprint>
	</monogr>
	<note>in SIG-MOD</note>
</biblStruct>

<biblStruct xml:id="b36">
	<monogr>
		<title level="m" type="main">Social computing data repository at asu</title>
		<author>
			<persName><forename type="first">R</forename><surname>Zafarani</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Liu</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2009">2009</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b37">
	<analytic>
		<title level="a" type="main">The biogrid interaction database: 2008 update</title>
		<author>
			<persName><forename type="first">B.-J</forename><surname>Breitkreutz</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Stark</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Reguly</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Boucher</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Breitkreutz</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Livstone</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><surname>Oughtred</surname></persName>
		</author>
		<author>
			<persName><forename type="first">D</forename><forename type="middle">H</forename><surname>Lackner</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Bähler</surname></persName>
		</author>
		<author>
			<persName><forename type="first">V</forename><surname>Wood</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">Nucleic acids research</title>
		<imprint>
			<biblScope unit="volume">36</biblScope>
			<biblScope unit="issue">1</biblScope>
			<biblScope unit="page" from="D637" to="D640" />
			<date type="published" when="2007">2007</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b38">
	<analytic>
		<title level="a" type="main">Arnetminer: extraction and mining of academic social networks</title>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Yao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Li</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Su</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2008">2008</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b39">
	<monogr>
		<title level="m" type="main">Large text compression benchmark</title>
		<author>
			<persName><forename type="first">M</forename><surname>Mahoney</surname></persName>
		</author>
		<ptr target="http://www.mattmahoney.net/text/text.html" />
		<imprint>
			<date type="published" when="2009">2009</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b40">
	<analytic>
		<title level="a" type="main">Automating the construction of internet portals with machine learning</title>
		<author>
			<persName><forename type="first">A</forename><forename type="middle">K</forename><surname>Mccallum</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Nigam</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Rennie</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Seymore</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">Information Retrieval</title>
		<imprint>
			<biblScope unit="volume">3</biblScope>
			<biblScope unit="issue">2</biblScope>
			<biblScope unit="page" from="127" to="163" />
			<date type="published" when="2000">2000</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b41">
	<analytic>
		<title level="a" type="main">Collective classification in network data</title>
		<author>
			<persName><forename type="first">P</forename><surname>Sen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Namata</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Bilgic</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Getoor</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Galligher</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Eliassi-Rad</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="j">AI magazine</title>
		<imprint>
			<biblScope unit="volume">29</biblScope>
			<biblScope unit="issue">3</biblScope>
			<biblScope unit="page" from="93" to="93" />
			<date type="published" when="2008">2008</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b42">
	<monogr>
		<title level="m" type="main">Efficient estimation of word representations in vector space</title>
		<author>
			<persName><forename type="first">T</forename><surname>Mikolov</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Corrado</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Dean</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1301.3781</idno>
		<imprint>
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b43">
	<analytic>
		<title level="a" type="main">Distributed representations of words and phrases and their compositionality</title>
		<author>
			<persName><forename type="first">T</forename><surname>Mikolov</surname></persName>
		</author>
		<author>
			<persName><forename type="first">I</forename><surname>Sutskever</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><forename type="middle">S</forename><surname>Corrado</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Dean</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b44">
	<analytic>
		<title level="a" type="main">Grarep: Learning graph representations with global structural information</title>
		<author>
			<persName><forename type="first">S</forename><surname>Cao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W</forename><surname>Lu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Xu</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">CIKM</title>
				<imprint>
			<date type="published" when="2015">2015</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b45">
	<monogr>
		<title level="m" type="main">Task-guided and path-augmented heterogeneous network embedding for author identification</title>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Sun</surname></persName>
		</author>
		<editor>WSDM</editor>
		<imprint>
			<date type="published" when="2017">2017</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b46">
	<monogr>
		<title level="m" type="main">Deep convolutional networks on graph-structured data</title>
		<author>
			<persName><forename type="first">M</forename><surname>Henaff</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Bruna</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Lecun</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1506.05163</idno>
		<imprint>
			<date type="published" when="2015">2015</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b47">
	<analytic>
		<title level="a" type="main">Convolutional neural networks on graphs with fast localized spectral filtering</title>
		<author>
			<persName><forename type="first">M</forename><surname>Defferrard</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Bresson</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Vandergheynst</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b48">
	<analytic>
		<title level="a" type="main">Multi-level graph convolutional networks for cross-platform anchor link prediction</title>
		<author>
			<persName><forename type="first">H</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Yin</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Sun</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Gabrys</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>Musial</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">KDD</title>
				<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b49">
	<analytic>
		<title level="a" type="main">Exploiting centrality information with graph convolutions for network representation learning</title>
		<author>
			<persName><forename type="first">H</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Yin</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><forename type="middle">V H</forename><surname>Nguyen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">W.-C</forename><surname>Peng</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Li</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICDE</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b50">
	<analytic>
		<title level="a" type="main">Representation learning on graphs with jumping knowledge networks</title>
		<author>
			<persName><forename type="first">K</forename><surname>Xu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Li</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Tian</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Sonobe</surname></persName>
		</author>
		<author>
			<persName><forename type="first">K</forename><surname>-I. Kawarabayashi</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Jegelka</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICML</title>
				<imprint>
			<date type="published" when="2018">2018</date>
			<biblScope unit="page" from="5449" to="5458" />
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b51">
	<monogr>
		<title level="m" type="main">Predict then propagate: Graph neural networks meet personalized pagerank</title>
		<author>
			<persName><forename type="first">J</forename><surname>Klicpera</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Bojchevski</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Günnemann</surname></persName>
		</author>
		<editor>ICLR</editor>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b52">
	<analytic>
		<title level="a" type="main">Data representation and learning with graph diffusion-embedding networks</title>
		<author>
			<persName><forename type="first">B</forename><surname>Jiang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">D</forename><surname>Lin</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">B</forename><surname>Luo</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">CVPR</title>
				<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b53">
	<monogr>
		<title level="m" type="main">Self-supervised learning: Generative or contrastive</title>
		<author>
			<persName><forename type="first">X</forename><surname>Liu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">F</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Hou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Mian</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Tang</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2021">2021</date>
			<publisher>TKDE</publisher>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b54">
	<monogr>
		<title level="m" type="main">A simple framework for contrastive learning of visual representations</title>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Kornblith</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Norouzi</surname></persName>
		</author>
		<author>
			<persName><forename type="first">G</forename><surname>Hinton</surname></persName>
		</author>
		<idno type="arXiv">arXiv:2002.05709</idno>
		<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b55">
	<monogr>
		<title level="m" type="main">Contrastive multi-view representation learning on graphs</title>
		<author>
			<persName><forename type="first">A</forename><forename type="middle">K</forename><surname>Sankararaman</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>De</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Xu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">R</forename><forename type="middle">W</forename><surname>Huang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Goldstein</surname></persName>
		</author>
		<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
	<note type="report_type">ICML</note>
</biblStruct>

<biblStruct xml:id="b56">
	<monogr>
		<title level="m" type="main">Deep graph contrastive representation learning</title>
		<author>
			<persName><forename type="first">Y</forename><surname>Zhu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Xu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">F</forename><surname>Yu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Liu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">S</forename><surname>Wu</surname></persName>
		</author>
		<author>
			<persName><forename type="first">L</forename><surname>Wang</surname></persName>
		</author>
		<idno type="arXiv">arXiv:2006.04131</idno>
		<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b57">
	<analytic>
		<title level="a" type="main">Graph contrastive learning with augmentations</title>
		<author>
			<persName><forename type="first">Y</forename><surname>You</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Sui</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Wang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Shen</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">NIPS</title>
				<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b58">
	<analytic>
		<title level="a" type="main">Graph contrastive learning automated</title>
		<author>
			<persName><forename type="first">Y</forename><surname>You</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Chen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Shen</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Z</forename><surname>Wang</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICML</title>
				<imprint>
			<date type="published" when="2021">2021</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b59">
	<analytic>
		<title level="a" type="main">Sub-graph contrast for scalable self-supervised graph representation learning</title>
		<author>
			<persName><forename type="first">Y</forename><surname>Jiao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Xiong</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">T</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Zhu</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICDM</title>
				<imprint>
			<date type="published" when="2020">2020</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b60">
	<analytic>
		<title level="a" type="main">Making a science of model search: Hyperparameter optimization in hundreds of dimensions for vision architectures</title>
		<author>
			<persName><forename type="first">J</forename><surname>Bergstra</surname></persName>
		</author>
		<author>
			<persName><forename type="first">D</forename><surname>Yamins</surname></persName>
		</author>
		<author>
			<persName><forename type="first">D</forename><surname>Cox</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">ICML</title>
				<imprint>
			<date type="published" when="2013">2013</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b61">
	<analytic>
		<title level="a" type="main">Towards automatically-tuned neural networks</title>
		<author>
			<persName><forename type="first">H</forename><surname>Mendoza</surname></persName>
		</author>
		<author>
			<persName><forename type="first">A</forename><surname>Klein</surname></persName>
		</author>
		<author>
			<persName><forename type="first">M</forename><surname>Feurer</surname></persName>
		</author>
		<author>
			<persName><forename type="first">J</forename><forename type="middle">T</forename><surname>Springenberg</surname></persName>
		</author>
		<author>
			<persName><forename type="first">F</forename><surname>Hutter</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">Workshop on Automatic Machine Learning</title>
				<imprint>
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
</biblStruct>

<biblStruct xml:id="b62">
	<monogr>
		<title level="m" type="main">Graphnas: Graph neural architecture search with reinforcement learning</title>
		<author>
			<persName><forename type="first">Y</forename><surname>Gao</surname></persName>
		</author>
		<author>
			<persName><forename type="first">H</forename><surname>Yang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">P</forename><surname>Zhang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">C</forename><surname>Zhou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Y</forename><surname>Hu</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1904.09981</idno>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b63">
	<monogr>
		<title level="m" type="main">Auto-gnn: Neural architecture search of graph neural networks</title>
		<author>
			<persName><forename type="first">K</forename><surname>Zhou</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><surname>Song</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Huang</surname></persName>
		</author>
		<author>
			<persName><forename type="first">X</forename><surname>Hu</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1909.03184</idno>
		<imprint>
			<date type="published" when="2019">2019</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b64">
	<monogr>
		<title level="m" type="main">Neural architecture search with reinforcement learning</title>
		<author>
			<persName><forename type="first">B</forename><surname>Zoph</surname></persName>
		</author>
		<author>
			<persName><forename type="first">Q</forename><forename type="middle">V</forename><surname>Le</surname></persName>
		</author>
		<idno type="arXiv">arXiv:1611.01578</idno>
		<imprint>
			<date type="published" when="2016">2016</date>
		</imprint>
	</monogr>
	<note type="report_type">arXiv preprint</note>
</biblStruct>

<biblStruct xml:id="b65">
	<analytic>
		<title level="a" type="main">His main research interests include graph neural networks and representation learning. Yukuo Cen is a PhD candidate in the Department of Computer Science and Technology, Tsinghua University. He got his bachelor degree in Computer Science and Technology from Tsinghua University. His research interests include social influence and graph embedding. Yuxiao Dong received his Ph</title>
		<author>
			<persName><forename type="first">J</forename><surname>Močkus</surname></persName>
		</author>
	</analytic>
	<monogr>
		<title level="m">Optimization techniques IFIP technical conference</title>
				<imprint>
			<publisher>Springer</publisher>
			<date type="published" when="1975">1975. 2017</date>
		</imprint>
		<respStmt>
			<orgName>Computer Science and Technology, Tsinghua University ; D. in Computer Science from University of Notre Dame</orgName>
		</respStmt>
	</monogr>
	<note>He is a research scientist at Facebook AI, Seattle, was previously a senior researcher at Microsoft Research, Redmond. His research focuses on data mining, representation learning, and networks. with an emphasis developing machine learning models to addressing problems in large-scale graph systems</note>
</biblStruct>

				</listBibl>
			</div>
		</back>
	</text>
</TEI>
"""

paper_json= """{
        "_id": "61dbf1dcd18a2b6e00d9f311",
        "title": "Automated Unsupervised Graph Representation Learning",
        "references": [
            "58437722ac44360f1082efeb",
            "5b67b45517c44aac1c860876",
            "5e8d8e6d9fced0a24b5d669e",
            "53e9b253b7602d9703cf4028",
            "5736977f6e3b12023e66632b",
            "57aa28de0a3ac518da9896d5",
            "5a260c8117c44a4ba8a30f54",
            "62376b725aee126c0f0a7412",
            "5bdc31b417c44a1f58a0b4e9",
            "5b8c9f4a17c44af36f8b6a96",
            "5d9edc8347c8f76646042a37",
            "5d4d46fb3a55acff992fde2b",
            "603e2f2191e01129ef28fecc",
            "5bdc319c17c44a1f58a0a1b7",
            "558ba88be4b00c3c48ddc0f3",
            "53e9b254b7602d9703cf70bb",
            "6001711bd4150a363c49b450",
            "5d3ed25a275ded87f97deba4",
            "5d3ed25a275ded87f97deb56",
            "5db929b747c8f766461fa94f",
            "53e9b527b7602d970405d9f8",
            "53e9b3fdb7602d9703ef0efb",
            "5e5e18b393d709897ce28ad3",
            "5e5e189a93d709897ce1e760",
            "53e9b3f5b7602d9703ee3407",
            "5cf48a40da56291d582a2f8e",
            "5e9661119fced0a24bb3f157",
            "53e9bd82b7602d9704a283df",
            "605058cc9e795e84274fd10f",
            "53e9b2ffb7602d9703dc29f7",
            "53e9a5afb7602d9702edacce",
            "53e9b6b4b7602d97042394bc",
            "53e9acc4b7602d97036a1037",
            "53e9b108b7602d9703b85b88",
            "58d82fcbd649053542fd67e0",
            "573695fd6e3b12023e511373",
            "57a4e91aac44365e35c97c6e",
            "5cfa5b985ced2477cb3c5175",
            "5b67b47917c44aac1c8637c6",
            "5ce2d032ced107d4c635260c",
            "5da2f8aa3a55ac3402d8c165",
            "5f993af691e011a3fbe2fb01",
            "60bdde338585e32c38af4f97",
            "5f6b5b0f91e011bf6740cc4a",
            "53e9b873b7602d9704442198",
            "5cede10eda562983788eea63",
            "58d82fc8d649053542fd59b8"
        ],
        "authors": [
            {
                "name": "Zhenyu Hou",
                "org": "Tsinghua University"
            },
            {
                "name": "Yukuo Cen",
                "org": "Tsinghua University"
            },
            {
                "name": "Jie Tang"
            }
        ],
        "year": 2021
    },
"""

example_format = """
    {
		"<example-paper-id>": []
	}
"""

response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": f"You are a classification AI that evaluates the ref-sources for xml formatted research papers. A reference is considered a ref-source if it has significant impact on the xml paper's content. Each paper can have multiple, one, or no ref-sources. Most sources are probably not ref-sources. Example response format: {example_format}. Follow the format exactly, it must be properly formatted json."},
        {"role": "user", "content": f"Identify the ref-sources. xml-paper: \n { xml_paper }\n\n json: { paper_json }. \n In the order that they are listed in the provided json, assign a 1 for ref-source and 0 for not."}
    ],
)

print(response.choices[0].message.content)