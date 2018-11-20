Operations available as per bindings based on protocols (SOAP1.1 and SOAP1.2)
can be inspected using the below command to get an overview of all available
operations and their call signatures.

```bash
python -mzeep http://www.dneonline.com/calculator.asmx?wsdl
```

Detailed Documentation is available at
https://python-zeep.readthedocs.io/en/master/index.html

Following code can be used to get the response

```python
from zeep import Client
client = Client('http://www.dneonline.com/calculator.asmx?wsdl')
# if you inspected the available operations as per the applicable binding
response=client.service.Add(intA=2, intB=3)
# response should return the result of the Add operation
```

Installation of Zeep required installation of `libxml2-devel` and `libxslt-devel`
using `pacman` on my `git-for-windows-sdk`

```bash
pacman -S libxml2-devel libxslt-devel
```

There has been no need to install any extras as highlighted in the document.


