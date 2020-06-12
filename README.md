# Analysis Libraries Interface Framework

Welcome to **ALIF**, the framework that interfaces between the analysis libraries
used in LIP-Coimbra. Hopefully, your work will be speeded up by the usage of it.

## Setup

To use **ALIF**, Anaconda needs to be installed in your system. Once that is
done, you need te create a `conda` environment from the `CERN.yml` file:

```bash
conda env create -f CERN.yml

source activate CERN
```

After that you should be good to go.

## Testing

**ALIF** comes with test suite, that checks if most of the functionalities of
the framework are working (if you come up with extra tests, do not hesitate to
add them!). After setting up your system, you should run the tests to see if
everything is working correctly.

To do that, go to the `test/` folder and do:

```bash
python -m unittest test_*
```

If there are no errors, carry on. If there are, you need to find why.

## Running

So far, **ALIF** interfaces between `LStore` (where the samples are stored),
`LipCbrAnalysis` (our main analysis toolkit) and `TRexFitter` (an ATLAS toolkit).
There is also a `Plotting` interface, that plots every variable in a root file
out of `LipCbrAnalysis`. It is slow, though.


The way **ALIF** is thought out is that `LipCbrAnalysis` is the main hub of the
analysis. It gets its input root files from `LStore` and its output root files
are used (so far) as `TRexFitter` input. As will be seen later on, a `TRexFitter`
job can use some files of another `TRexFitter` job, but a full integration with
its output, for extra libraries added in the future, for example, will only
be built when needed.

To run **ALIF**, you need an options file in the `input_txt/` folder (the options
will be shown later). When you have that, go into the `src/` folder and do:

```bash
python main.py ../input_txt/myfile.txt
```
where `myfile.txt` is the name of your options file.

The output of every job will be saved in the `../results/` folder, with the
appropiate structure built. Besides that, every input text file used to
specify the job will be copied to the job folder in the `../results/` folder.

## Options

A typical input options file might have this structure:

```
Job: LStore
  Output: 001
  Description: Definition of the analysis samples
  Year: 151617
  MCYear: 16
  Samples: samples.txt

Job: LipCbrAnalysis
  Output: 001.001
  Description: Initial analysis
  Year: 151617
  MCYear: 16
  Samples: samples.txt
  CutFile: docuts.cxx
  SamplesToRun: 301, 403

Job: TRexFitter
  Output: 001.002
  Description: Zee+jets fit
  Year: 151617
  MCYear: 16
  Samples: samples.txt
  Regions: regions.txt
  NormFactors: normfactors.txt
```

The list of options are explained now. The main option `Job` is used to specify
which type of job to run. So far, these are available:

* LStore
* LipCbrAnalysis
* TRexFitter
* Plotting

Each of these types has its own options (although they share some). All the
options implemented are shown here. For details, see `docs/` folder. The
required options are in **bold**. For those that are not required, the default
option value is in **bold**.

* Job: LStore
  * **Output**: name
  * **Description**: One line description
  * Year: 15 | 16 | 17 | **1516** | 151617
  * MCYear: 15 | **16**
  * Samples: samples.txt
  * SystWeights: True | **False** (NOT IMPLEMENTED YET)
  * SystTrees: True | **False** (NOT IMPLEMENTED YET)

* Job: LipCbrAnalysis
  * **Output**: name
  * **Description**: One line description
  * **Samples**: samples.txt
  * **CutFile**: docuts.cxx
  * Year: 15 | 16 | 17 | **1516** | 151617
  * MCYear: 15 | **16**
  * Tree: **nominal**
  * SystTree: **does nothing**
  * SystWeight: **[]**
  * SamplesToRun: **all**
  * RegionsToRun: **all**
  * Compile: **True** | False

* Job: TRexFitter
  * **Output**: name
  * **Description**: One line description
  * **Samples**: samples.txt
  * **Input**: input.txt
  * **Regions**: regions.txt
  * **NormFactors**: normfactors.txt
  * Year: 15 | 16 | 17 | **1516** | 151617
  * MCYear: 15 | **16**
  * SystTree: **[]**
  * SystWeight: **[]**
  * SystAnalysis: **""**
  * Asimov: True | **False**
  * Fit: **SPLUSB**|BONLY/**CRSR**|CRONLY
  * Limit: True | **False**
  * ShowData: **True** | False
  * Luminosity: **0**
  * FullAsimov: True | **False**
  * ReadFrom: **HIST** | NTUP
  * FileSuffix: **""**
  * ShowYields: **True** | False
  * PrepareSamples: **True** | False | Only
  * NewFileSuffix: **""**

* Job: Plotting
  * **Output**: name
  * **Description**: One line description
  * **Samples**: samples.txt
  * **CutFile**: docuts.cxx
  * **Input**: input.txt
  * Year: 15 | 16 | 17 | **1516** | 151617
  * MCYear: 15 | **16**
  * PlotAll: True | **False**
  * ShowData: **True** | False
  * PlotSignalStacked: **True** | False
  * FromCut: **0**
  * OrderSamples: True | **False**
  * PlotTest: **does nothing** | Ratio (NOT IMPLEMENTED YET)
  * ShowOverUnderFlow: True | **False**
  * Cuts: **[]**

If you want some lines to be ignored, put a `%` at the beginning of it.

# To Do

## General
- [ ] Find a way so that it does not matter if there is a blank line at the
end of input files

## LipCbrAnalysis

## TRexFitter
