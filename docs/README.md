# ALIF Documentation

Here you will find the details of every option of every job.

## Table of Contents

- [LStore](#lstore)
  - [Output](#lstore-output)
  - [Description](#lstore-description)
  - [Year](#lstore-year)
  - [MCYear](#lstore-mcyear)
  - [Samples](#lstore-mcyear)
  - [SystTrees](#lstore-systtrees)
  - [SystWeights](#lstore-systweights)
- [LipCbrAnalysis](#lipcbranalysis)
  - [Output](#lipcbranalysis-output)
  - [Description](#lipcbranalysis-description)
  - [Samples](#lipcbranalysis-samples)
  - [CutFile](#lipcbranalysis-cutfile)
  - [Year](#lipcbranalysis-year)
  - [MCYear](#lipcbranalysis-mcyear)
  - [Tree](#lipcbranalysis-tree)
  - [SystTree](#lipcbranalysis-systtree)
  - [SystWeight](#lipcbranalysis-systweight)
  - [SamplesToRun](#lipcbranalysis-samplestorun)
  - [RegionsToRun](#lipcbranalysis-regionstorun)
  - [Compile](#lipcbranalysis-compile)
- [TRexFitter](#trexfitter)
  - [Output](#trexfitter-output)
  - [Description](#trexfitter-description)
  - [Samples](#trexfitter-samples)
  - [Input](#trexfitter-input)
  - [Regions](#trexfitter-regions)
  - [NormFactors](#trexfitter-normfactors)
  - [Year](#trexfitter-year)
  - [MCYear](#trexfitter-mcyear)
  - [SystTree](#trexfitter-systtree)
  - [SystWeight](#trexfitter-systweight)
  - [SystAnalysis](#trexfitter-systanalysis)
  - [Asimov](#trexfitter-asimov)
  - [Fit](#trexfitter-fit)
  - [Limit](#trexfitter-limit)
  - [ShowData](#trexfitter-showdata)
  - [Luminosity](#trexfitter-luminosity)
  - [FullAsimov](#trexfitter-fullasimov)
  - [POI](#trexfitter-poi)
  - [ReadFrom](#trexfitter-readfrom)
  - [FileSuffix](#trexfitter-filesuffix)
  - [ShowYields](#trexfitter-showyields)
  - [PrepareSamples](#trexfitter-preparesamples)
  - [NewFileSuffix] (#trexfitter-newfilesuffix)
- [Plotting](#plotting)
  - [Output](#plotting-output)
  - [Description](#plotting-description)
  - [Samples](#plotting-samples)
  - [CutFile](#plotting-cutfile)
  - [Input](#plotting-input)
  - [Year](#plotting-year)
  - [MCYear](#plotting-mcyear)
  - [PlotAll](#plotting-plotall)
  - [ShowData](#plotting-showdata)
  - [PlotSignalStacked](#plotting-plotsignalstacked)
  - [FromCut](#plotting-fromcut)
  - [OrderSamples](#plotting-ordersamples)
  - [PlotTest](#plotting-plottest)
  - [ShowOverUnderFlow](#plotting-showoverunderflow)
  - [Cuts](#plotting-cuts)

## LStore

Creates the necessary files that LipCbrAnalysis uses.

<a name="lstore-output"></a>
### Output

* **Required**
* **Possible values**: Anything, but if it is equal to a sequence of numbers grouped
in three and separated by a dot (like 001.125.874), then when saving the Output
name and Description to `results/results.txt`, the entries are put in numerical
order (see template).
* **Description**: Name of subfolder if `results/` where output is stored. Also
creates an entry in `results/results.txt` for the job.
* **Template**: `results.txt` (the numbers on the right side are not written to the
file)

```
001: Description 1               (1)
001.001: Description 1.1         (2)
001.002: Description 1.2         (3)
002: Description 2               (4)
002.001: Description 2.1         (5)
002.001.001: Description 2.1.1   (6)
```

  1. Output = 001
  2. Output = 001.001
  3. Output = 001.002
  4. Output = 002
  5. Output = 002.001
  6. Output = 002.001.001

To [Table of Contents](#table-of-contents)
<a name="lstore-description"></a>
### Description

* **Required**
* **Possible values**: Anything
* **Description**: One line description of job, to be written in `results/results.txt`,
as explained in Output

To [Table of Contents](#table-of-contents)
<a name="lstore-year"></a>
### Year

* **Default**: 1516
* **Possible values**: 15, 16, 17, 1516, 151617
* **Description**: The data year to be used. Affects luminosity in LipCbrAnalysis
and TRexFitter

To [Table of Contents](#table-of-contents)
<a name="lstore-mcyear"></a>
### MCYear

* **Default**: 16
* **Possible values**: 15, 16
* **Description**: The MC version to be used. Affects variables in LipCbrAnalysis

To [Table of Contents](#table-of-contents)
<a name="lstore-samples"></a>
### Samples

* **Default**: ""
* **Possibles values**: Name of file in `input_txt/`
* **Description**: Name of file to be parsed to obtained the details of the
samples to be used. A `cxx` file is then created with sample codes, that will
be used in LipCbrAnalysis. If necessary, the file can also include details for
TRexFitter. However, when parsed within a LStore job, those details are ignored.
You should put only MC samples here. Data is handled within the code.
* **Template**: `samples.txt`

```
HistoFile: signal_sW                        (1)
Type: SIGNAL                                (2)
Title: t#bar{t} #rightarrow sWbW            (3)
FillColor: 50                               (4)
DSID: 111111                                (5)
      111120-111130                         (6)
MCName: Sherpa_blabla1                      (7)
        Sherpa_blabla2                      
Group: Important samples                    (8)
SampleCode: 300                             (9)
                                            (10)
HistoFile: background_WtZ
.
.
.
```
1. Name of subfolder where processed sample root files will be stored
  * Can be anything
  * Used in LStore, LipCbrAnalysis and TRexFitter
2. Type of sample
  * Can be SIGNAL, BACKGROUND and SYSTEMATIC. This last one is not written in
  the samples section of the TRexFitter config file.
  * Used in TRexFitter
3. Title of sample to be used in the plots
  * Can be anything
  * Used in TRexFitter
4. Fill color of the sample
  * Can be any color supported by ROOT
  * Used in TRexFitter
5. DSID's of the samples. These are translated into MCName's, which are used to
to create the `cxx` file.
  * Can be any DSID present in the DefineSamples file in `/lstore/atlas/sg/`.
  The name of the folder is defined within the code.
  * Used in LStore
  6. Supports intervals
7. MC variable names. These are the translation of the DSID's
  * Can by any MC variable name in the DefineSamples file in `/lstore/atlas/sg/`
  * Used in LStore
8. Group to which the sample belongs.
  * Can be Anything
  * Used in TRexFitter
9. Sample code with which the LipCbrAnalysis code recognises the sample
  * Can be any number, but I follow some guidelines when choosing them
    * 1-199: Reserved for individual MC variables (do not use)
    * 200-299: Truth samples
    * 300-399: Signal samples
    * 400-499: Background samples
10. You must leave a blank line between samples. Also do not leave a blank line
at the end of the file. Screws stuff.


To [Table of Contents](#table-of-contents)
<a name="lstore-systtrees"></a>
### SystTrees

* **Default**: False
* **Possible values**: True, False
* **Description**: Makes a list with all the systematic trees (NOT IMPLEMENTED)

To [Table of Contents](#table-of-contents)
<a name="lstore-systweights"></a>
### SystWeights

* **Default**: False
* **Possible values**: True, False
* **Description**: Makes a list with all the systematic weights (NOT IMPLEMENTED)

To [Table of Contents](#table-of-contents)
## LipCbrAnalysis

Creates the necessary `submit*.sh` and scratch files for the LipCbrAnalysis to
run, compiles and runs it

<a name="lipcbranalysis-output"></a>
### Output

See [Output](#lstore-output)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-description"></a>
### Description

See [Description](#lstore-description)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-samples"></a>
### Samples

See [Samples](#lstore-samples)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-cutfile"></a>
### CutFile

* **Required**
* **Possible values**: Name of file in `analysis_deploy/AnalysisCode/DoCuts/`
* **Description**: Name of cuts file to use. From this file, **ALIF** gets
`MaxCuts` and the regions (see template). Since, to get `MaxCuts`, the framwork
counts the number of `LastCut++`, *do not* comment any line that has that.
* **Template**: `docuts.cxx`

```c++
/*                              (1)
Begin Regions                   (2)
1: SR                           (3)
2: FakesCR
3: ZjetsCR
End Regions                     (4)
*/
...
Cut1
...
LastCut++;                      (5)
...
Cut2
...
LastCut++;                      (5)
```

1. The regions name and code should be commented at the top of the cuts file,
with a multi-line comment (not multiple single line comments)
2. Before giving the regions name and code, there should be a line with
*Begin Regions*
3. First the code of the region, then a colon, then the name of the region, with
no blank spaces
4. At the end of the definition of the regions, there should be a line with
*End Regions*
5. There are two `LastCut++` in this file, so `MaxCuts = 2`

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-year"></a>
### Year

See [Year](#lstore-year)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-mcyear"></a>
### MCYear

See [Year](#lstore-mcyear)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-tree"></a>
### Tree

* **Default**: nominal
* **Possible values**: `nominal`, `particleLevel`, `all`
* **Description**: Name of the tree to use in the input root files. If it is
equal to `all`, then runs for nominal, for all systematic weights and all
systematic trees. The value of this option is overridden if `SystTree` option
has a value, so, if you want to run the `nominal` tree and all the systematic
trees, then you must have two jobs. When using `particleLevel` option, the
name of the output files is still `nominal`, because the other types of jobs can
only use this name.

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-systtree"></a>
### SystTree

* **Default**: does nothing
* **Possible values**: Any systematic tree in the list `syst_trees` in
`systematics.py`, and `all`
* **Description**: Name of systematic tree to use. Overrides `Tree` option if
given a value. If it is a comma separated list, runs for every element of the
list. If `all`, then runs for every systematic tree.

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-systweight"></a>
### SystWeight

* **Default**: []
* **Possible values**: Any systematic weight in the list `syst_weights` in
`systematics.py`, and `all`
* **Description**: Name of systematic weight to use. If it is a comma separated list,
runs for every element of the list. If `all`, then runs for every systematic
weight.

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-samplestorun"></a>
### SamplesToRun

* **Default**: all
* **Possible values**: Any sample code in the given `Samples` file, plus `all`
and `data`
* **Description**: Comma separated list of samples codes to run. If it is equal
to `all`, then runs for everything (including `data`)

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-regionstorun"></a>
### RegionsToRun

* **Default**: all
* **Possible values**: Any region names in the given `CutFile` file, plus `all`
* **Description**: Comma separated list of region names to run. If it is equal
to `all`, then runs for everything

To [Table of Contents](#table-of-contents)

<a name="lipcbranalysis-compile"></a>
### Compile

* **Default**: True
* **Possible values**: True, False
* **Description**: Whether to compile `AnalysisCode` before running the jobs.
It also does not rewrite the `scratch` and `submit_files` folders. Could be used
when you need to run different jobs for different kinds of samples (`nominal`
and `particleLevel`, for example), but want them in the same output folder. You
should be careful to check if the cuts file for the job is the one you really want.

To [Table of Contents](#table-of-contents)

## TRexFitter

Creates the necessary config files for TRexFitter and runs them

<a name="trexfitter-output"></a>
### Output

See [Output](#lstore-output)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-description"></a>
### Description

See [Description](#lstore-description)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-samples"></a>
### Samples

See [Samples](#lstore-samples)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-input"></a>
### Input

* **Required**
* **Possible values**: Any file in `input_txt/`
* **Description**: File that indicates where to get the samples, and what to do
with them before running TRexFitter
* **Template**: `input.txt`

```
Sample: all                         (1)
Region: all                         (2)
Folder: 001.002                     (3)
                                    (4)
Sample: signal_sW                   (5)
Region: SR                          (6)
Scale: 5.2                          (7)

Sample: background_bWbW
Regions: SR, bWbWCR                 (8)
Cut: 2-10                           (9)
Scale: "001.001"                    (10)

Sample: background_ttZ
Folder: 001.003
Cut: 2-4, 5, 10-12                  (11)
ScaleBinByBin: 2->5.5, 4->"001.002" (12)

Sample: background_WtZ
Region: ZjetsCR
ExcludeFromSystematics: True        (13)
ExcludeFromRegions: True            (14)

Sample: background_Z+jets
Scale: (+ (* 1.2 "001.001") 1.4)    (15)

Sample: background_ttH
Signal: True                        (16)

Sample: background_noidea           
Scale: "001.004@norm_factor"        (17)
```

* Sample
  <ol start="1">
  <li>If all, then applies option to every sample in Samples file.
  If no Sample is indicated, then this is the Default</li>
  </ol>
  <ol start="5">
  <li> Indicate the HistoFile parameter in Samples file. This could also be a
  comma-separated list </li>
  </ol>
* Region
  <ol start="2">
  <li>If all, then applies option to every region specified in the Regions file
  (obtained by looking at the HistoPathSuff option). This is the default value
  if no Region is specified. The variables indicated in the HistoName option
  are the only ones used for the options in this file</li>
  </ol>
  <ol start="6">
  <li>Any region in Regions file can be specified</li>
  </ol>
  <ol start="8">
  <li>Could be a comma-separated list</li>
  </ol>
* Folder
  <ol start="3">
  <li>Folder from where to get the histograms. Must exist (of course). It goes
  through the `MCYear/Year/Region/Sample/` directory structure</li>
  </ol>
* Scale
  <ol start="7">
  <li>Used to scale histograms of the specified regions and samples by the amount
  given</li>
  </ol>
  <ol start="10">
  <li> Could be a name of the `results/` sub-folder. Must be enclosed by double
  quotation marks ("). It gets the value of `#mu` in the file `job_001.001.txt`
  inside `001.001/001.001_TRexFitter/Fits/`</li>
  </ol>
  <ol start="15">
  <li> Supports simple symbolic math (addition, multiplication, subtraction
  and division), in Scheme programming language format. Also supports square
  root (with the v operator)</li>
  </ol>
  <ol start="17">
  <li> If you used several normalization factors in a fit, it is possible
  to get one of them, by using `@` after the name of the sub-folder (no spaces)
  and then the name of the normalization factor you want.</li>
  </ol>
* Cut
  <ol start="9">
  <li>Indicates interval to use </li>
  </ol>
  <ol start="11">
  <li> Could also be a list of intervals</li>
  </ol>
* ScaleBinByBin
  <ol start="12">
  <li> Comma-separated list of scale factors applied to certain bins. Format is
  bin->scale_factor </li>
  </ol>
* ExcludeFromSystematics
  <ol start="13">
  <li> Does not use given sample(s) in the systematics </li>
  </ol>
* ExcludeFromRegions
  <ol start="14">
  <li> Excludes given sample(s) from given region(s) </li>
  </ol>
* Signal
  <ol start="16">
  <li> Uses the given sample(s) as signal, instead of the one(s) indicated in
  the samples file </li>
  </ol>

<ol start="4">
<li>Leave a blank line between group of options. DO NOT LEAVE A BLANK LINE AT THE
END OF THE FILE </li>
</ol>
To [Table of Contents](#table-of-contents)

<a name="trexfitter-regions"></a>
### Regions

* **Required**
* **Possible values**: Any file in `input_txt/`
* **Description**: File with regions used in the fit. It should be exactly as
in TRexFitter config files. I thought each one would be too customized for each
fit to be automated.
* **Template**: `regions.txt`

```
Region: "ZjetsCR_fakes"
  Type: SIGNAL
  HistoName: "sel07_mZ"                                 (1)
  HistoPathSuff: "ZjetsCR/"                             (2)
  VariableTitle: "m_{ll} [GeV]"
  Label: "Z+jets CR Fake Leps"
  ShortLabel: "ZjetsCR_fakes"
  Binning: 60,65,70,75,80,85,90,95,100,105,110,115,120
  BinWidth: 5
```
1. This is, of course, required. ROOT will give an error if it does not exist.
2. This option is also required. It should be the name of the region subfolder.
The `/` is necessary, since TRexFitter does not add it.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-normfactors"></a>
### NormFactors

* **Required**
* **Possible values**: Any file in `input_txt/`
* **Description**: File with NormFactors used in the fit. It should be exactly as
in TRexFitter config files. I thought each one would be too customized for each
fit to be automated.
* **Template**: `normfactors.txt`

```
NormFactor: "#mu"                   (1)
  Title: #mu
  Nominal: 1
  Min: 0.5
  Max: 4
  Samples: signal_sW                (2)
```
1. There should always be a normfactor `#mu`, as it is the POI defined. Might
change that later on.
2. This is the `HistoFile` option in the `Samples` input file.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-year"></a>
### Year

See [Year](#lstore-year)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-mcyear"></a>
### MCYear

See [Year](#lstore-mcyear)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-systtree"></a>
### SystTree

* **Default**: []
* **Possible values**: Any element of the list `syst_trees` in `systematics.py`,
minus the "up" and "down"
* **Description**: Comma separated list of systematic trees to use. If `all`,
then uses every tree. When adding other trees to the `syst_trees` list, you
should be careful with the "down" and "up" endings. Right now, it works
with both "down" and "Down" endings (and, equivalently, with "up" and "Up"). If
the tree you are adding has a different ending, you must modify that in the code.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-systweight"></a>
### SystWeight

* **Default**: []
* **Possible values**: Any element of the list `syst_weights` in `systematics.py`,
minus the "up" and "down"
* **Description**: Comma separated list of systematic weights to use. If `all`,
then uses every weight. When adding other weights to the `syst_weights` list, you
should be careful with the "down" and "up" endings. Right now, it works
with both "down" and "DOWN" endings (and, equivalently, with "up" and "UP"). If
the tree you are adding has a different ending, you must modify that in the code.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-systanalysis"></a>
### SystAnalysis

* **Default**: ""
* **Possible values**: Any file in `input_txt\`
* **Description**: Systematics specific to the analysis. Should be a text file
with the systematics as TRexFitter requires them.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-asimov"></a>
### Asimov

* **Default**: False
* **Possible values**: True, False
* **Description**: If it does an Asimov Fit and/or Limit. Adds `data` entry
to Samples if False. If True, then does show Data/MC ratio plot.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-fit"></a>
### Fit

* **Default**: SPLUSB/CRSR
* **Possible values**: SPLUSB/CRSR, SPLUSB/CRONLY, BONLY/CRSR, BONLY/CRONLY
* **Description**: Fit options for TRexFitter config file

To [Table of Contents](#table-of-contents)

<a name="trexfitter-limit"></a>
### Limit

* **Default**: False
* **Possible values**: True, False
* **Description**: If it does a limit calculation

To [Table of Contents](#table-of-contents)

<a name="trexfitter-showdata"></a>
### ShowData

* **Default**: True
* **Possible values**: True, False
* **Description**: If data points are shown in plots. If False, then it doesn't
show the Data/MC ratio plot as well.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-luminosity"></a>
### Luminosity

* **Default**: 0
* **Possible values**: Any number
* **Description**: If it is different than 0, then the `LumiLabel` option in the
config file will have this value (in fb<sup>-1</sup>). If it is 0, then uses
the default value for the `Year` chosen. See `TRexFitter` code for these values.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-fullasimov"></a>
### FullAsimov

* **Default**: False
* **Possible values**: True, False
* **Description**: Whether it creates asimov data histograms using both background
and signal (the Asimov option in TRexFitter uses only background)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-poi"></a>
### POI
* **Default**: "#mu"
* **Possible values**: Anything really
* **Description**: Name of parameter of interest to use in fit/limit.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-readfrom"></a>
### ReadFrom

* **Default**: HIST
* **Possible values**: HIST, NTUP
* **Description**: Whether it gets values from an histogram or ntuple.
It does not put ntuple options in TRexFitter. Instead, it converts the tree
variables to histograms. In the regions file, the variables must then be
tree variables. If there is a FileSuffix option, it will need the files
without the suffix as well.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-filesuffix"></a>
### FileSuffix

* **Default**: empty string
* **Possible values**: Anything
* **Description**: String to add to the end of the root files
(nominal_filesuffix.root)

To [Table of Contents](#table-of-contents)

<a name="trexfitter-showyields"></a>
### ShowYields

* **Default**: True
* **Possible values**: True, False
* **Description**: Whether to show samples yields

To [Table of Contents](#table-of-contents)

<a name="trexfitter-preparesamples"></a>
### PrepareSamples

* **Default**: True
* **Possible values**: True, False, Only
* **Description**: Whether to prepare histograms for TRexFitter. Normally
used when they have already been created once, but the fit did not converge and
you need to run it again. Also has Only option, in case you need to prepare
samples from different types of files (like one directly from LipCbrAnalysis
and another from a neural network). This, as the name suggests, only prepares
the samples, without running TRexFitter.

To [Table of Contents](#table-of-contents)

<a name="trexfitter-newfilesuffix"></a>
### NewFileSuffix

* **Default**: empty string
* **Possible values**: Anything
* **Description**: New file suffix to add to root files.

To [Table of Contents](#table-of-contents)

## Plotting

Creates the necessary config files for TRexFitter and runs them

<a name="plotting-output"></a>
### Output

See [Output](#lstore-output)

To [Table of Contents](#table-of-contents)

<a name="plotting-description"></a>
### Description

See [Description](#lstore-description)

To [Table of Contents](#table-of-contents)

<a name="plotting-samples"></a>
### Samples

See [Samples](#lstore-samples)

To [Table of Contents](#table-of-contents)

<a name="plotting-cutfile"></a>
### CutFile

See [CutFile](#lipcbranalysis-cutfile)

To [Table of Contents](#table-of-contents)

<a name="plotting-input"></a>
### Input

* **Required**
* **Possible values**: Any file in `input_txt/`
* **Description**: File that indicates where to get the samples, and what to do
with them before running TRexFitter
* **Template**: `input.txt`

```
Sample: all                         
Region: all                         
Folder: 001.002                     

Sample: signal_sW                   
Region: SR                          
Test: True                          (1)
```

* Test
  1. If includes this variable in this region in the testing (NOT IMPLEMENTED
  YET)
* For all the other options, see [Input](#trexfitter-input)

To [Table of Contents](#table-of-contents)
<a name="plotting-year"></a>
### Year

See [Year](#lstore-year)

To [Table of Contents](#table-of-contents)

<a name="plotting-mcyear"></a>
### MCYear

See [Year](#lstore-mcyear)

To [Table of Contents](#table-of-contents)

<a name="plotting-plotall"></a>
### PlotAll

* **Default**: False
* **Possible values**: True, False
* **Description**: Whether to plot every variable in the root files, for every
region defined in the cuts file, and for every variable defined in the samples
file

To [Table of Contents](#table-of-contents)

<a name="plotting-showdata"></a>
### ShowData

* **Default**: True
* **Possible values**: True, False
* **Description**: Whether to plot data points, in addition to the MC samples

To [Table of Contents](#table-of-contents)

<a name="plotting-plotsignalstacked"></a>
### PlotSignalStacked

* **Default**: True
* **Possible values**: True, False
* **Description**: Whether to plot signal MC sample on the histogram stack or
apart from the other MC samples

To [Table of Contents](#table-of-contents)

<a name="plotting-fromcut"></a>
### FromCut

* **Default**: 0
* **Possible values**: Any integer greater or equal than 0 and not greater than
the MaxCuts obtained from the cuts file
* **Description**: Cut from which to start making the plots

To [Table of Contents](#table-of-contents)

<a name="plotting-ordersamples"></a>
### OrderSamples

* **Default**: False
* **Possible values**: True, False
* **Description**: Whether to plot the MC samples in descending order of number
of events (with the biggest ones at the bottom of the histogram)

To [Table of Contents](#table-of-contents)

<a name="plotting-plottest"></a>
### PlotTest

* **Default**: does nothing
* **Possible values**: Ratio
* **Description**: Whether to find the best cuts for every sample in every
variable, using the given method

To [Table of Contents](#table-of-contents)

<a name="plotting-showoverunderflow"></a>
### ShowOverUnderFlow

* **Default**: False
* **Possible values**: True, False
* **Description**: Whether to show the over/underflows as well. This adds
"w/ Over/Underflow" to the title of the plots

To [Table of Contents](#table-of-contents)

<a name="plotting-cuts"></a>
### Cuts

* **Default**: []
* **Possible values**: Comma-separated list of integers
* **Description**: List of selection levels to plot. Overrides [FromCut](#plotting-fromcut).

To [Table of Contents](#table-of-contents)
