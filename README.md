# keller-isd-tax-calculations
An attempt to understand where Keller ISDs tax revenue comes from

### Changelog
2/6/24 10PM: original post
2/7/25 10:45PM: added new file to calculate east side vs west side

## What's this all about

On 2/6/2025, Dylan Oleszak made the a [Facebook post](https://www.facebook.com/share/p/19zjjhdRfn/) with a claim that, "Keller accounts for only 25% of KISD but pays 45% of all KISD debt." 

That didn't sound right to me, so I set out to investigate. My goal is to provide data, and the method I used to arrive at my conclusions, so that anyone who wants to can replicate my work.

tl;dr: My calculations show that about 31% of KISD's tax revenue likely comes from inside the Keller city limits, and
69% comes from outside Keller proper.

## Background

Let's start with how "KISD debt" is paid. This term is somewhat vague since the district has both short-term debt and long-term debt and they are paid from different buckets of money, but by and large most of the 'debt' debate here has focused on bonds issued by the district. KISD issued $169.5 millin of debt in the 2014 bond and $315 million of debt in the 2019 bond. These bond issues were on top of additional debt the district had from previous debt issues. 

This debt is paid by tax revenues from property taxes the district assesses against real property in the district. To see how much of your property tax goes to this debt, go to www.tad.org and look up your property. You should see, in the Prperty Data section, under the Jurisdictions list, an entry for "Keller ISD (907)." Under the "$ Values" section of that page, there is a lnk to "Tarrant County Tax Office Account Information." Click on that link. That should take you to the Tarrant County Tax Assessor's page for your property account. In the lower "Property Tax Record" section click the "view breakdown" of your 2024 tax bill. You will see the total tax paid to Keller ISD.

However, The Keller ISD tax is actually TWO taxes: the "maintenance and operations," or "M&O" tax, and the "interest and sinking," or "I&S" tax. Debt repayment comes from the I&S tax. I have found no easy way to see the two separate taxes online. For 2024, I believe the M&O rate was $0.7575 per $100 of valuation and the I&S rate was $0.33 per $100 of valuation.

To verify your KISD taxes, do this with the information on that page:

(land value + improvement value - exemptions) * (I&S rate + M&O rate) / 100

When I do this calculation on my property it comes out within $8 of my tax bill; that's "close enough" for me.

So, to test Mr. Oleszak's hypotheses, we need to determine aggregate I&S revenue from various parts of the district and determine what portion of that revenue comes from "Keller."

## Methodology

I do not see that the Tax Assessor makes revenue figures downloadable from their website. (I'm sure it's public information but finding it will take time and effort and this post has already taken too much of my time and effort.) However, the Tarrant Appraisal District DOES make their data freely downloadable.

The difference is the TAD data shows (indirectly) how much was billed, the tax assessor's data would show how much was collected. If we can agree that these two numbers are reasonably close to each other, using TAD data should suffice for our calculations.

TAD data can be downloaded from https://www.tad.org/resources/data-downloads. I downloaded the 2024 Certified Data file "PropertyData-FullSet(Certified)" which I believe is going to give the most accurate data for this purpose. This is a 74MB .zip file that contains all of TAD's data on all real property for tax year 2024. Inside the .zip file is a single file, "PropertyData_2024.txt" that I extracted. This is a pipe-delimited file with a header. 

For reasons probably lost to time, the PropertyData file does not actually contain the address of the property. That information is in a separate file, the Supplemental Data file. And even this file doesn't contain the property's ZIP code.

Mr. Oleszak's claim requires us to define what he means by "Keller." For this purpose I chose to classify any real property with "KELLER" as the City field in the supplemental file as his target population.

Writing a computer program to read this data and make calculations on this file with this definition is reasonably straightforward. Because I need to join to reasonably large data files I chose to solve this problem in Python using the Spark library.

Now... my code is not perfect. From the data I have, I could not find a way to properly account for exemptions such as homestead exemptions that most of us have on our primary residence. However, as a first-order approximation, I think that this code is a reasonable starting point. I welcome input here and if anyone wants to form a working group to see if we can create better calculations please reach out to me.

## Conclusion

The output of this program is:

```
There are 17255 keller properties
There are 46760 non keller properties
    Keller value: 10269530553.0
Non Keller value: 22489900528.0
Percentage of Keller ISD taxes from properties in the City of Keller: 31.348317764151222
Percentage of Keller ISD taxes from properties not in the City of Keller: 68.65168223584878
```

So, by my admittedly rough calculations, Keller ISD gets about 68% of its tax revenue from outside Keller city limits.

I also admit that I do not fully understand my source data and my code may be based on incorrect assumptions.

I cannot make any meaninful comparison between my numbers and those generated by Moak Casey (which is the data source that Mr. Oleszak cited 
for his claim), because the KISD school board has not released the full Moak Casey report to the public and we have no information on
the methodology used by MK. I look forward to the public release of the report, which should allow us to reconcile the differences between
my calculations and theirs

## Future Improvments

If anyone wishes to take this a step forward, using data from the Tarrant County Tax Assessor is likely to provide a more accurate
answer to the question

## Does it matter?

At the end of the day, I fail to see how this information is relevant to the "split the district" issue.