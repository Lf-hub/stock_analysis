import requests

from django.shortcuts import render
from django.views.generic import View, CreateView

from core.forms import APIForm

from core.models import Assets, AssetsType, APIConnections, ImportFile, Companies

from core.operations.helpers import get_site, get_asset_type, get_assets, save_companies
from core.operations.process.import_file import DataImporter
from core.operations.processes import ConsultYahoo, ConsultAPI, PreviewPrice

from cryptocurrency.btc.value_btc import analyze_bitcoin


class IndexView(CreateView):
    model = ImportFile
    fields = ['file',]
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            file = request.FILES.get('file')
            file_type = request.FILES['file'].name.split('.')[-1]
            # Cria dataframe
            data = DataImporter(file,file_type).import_data()
            # Salva arquivo
            import_file_instance = ImportFile(file=file)
            import_file_instance.save()
            
            # Salva empresas na tabela
            # save_companies(data)
        return render(request, self.template_name, {'imported_data': data})


class APIProcessView(View):
    template_name = 'api_process.html'
    form = None

    def get_form(self):
        if not self.form:
            self.form = APIForm(self.request.GET)
        return self.form

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if 'yahoo' in kwargs.get('param'):
            if request.GET:
                site = get_site(request.GET.get('site'))
                asset_list = list(get_assets(request.GET.get('asset')).values_list('slug', flat=True))
                asset_type = get_asset_type(request.GET.get('asset_type'))
                if site.slug == 'yahoo':
                    ConsultYahoo().main(asset_list)
                elif site.slug == 'coingecko':
                    ConsultAPI().main()
        else:
            folder_path = "/home/carol/Área de Trabalho/projetos/stock_analysis/arquivos_teste"
            PreviewPrice(folder_path).main()

        return render(request, self.template_name, {'form': form})

class CryptoCurrency(View):
    template_name = 'crypto/index.html'

    def get(self, request, *args, **kwargs):
        crypto_codes = Assets.objects.filter(asset_type__slug='cripto')
        data = []
        for code in crypto_codes:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={code.slug}&vs_currencies=brl"
            response = requests.get(url)
            if response.status_code in [200,2001]:
                value = float(response.json().get(f'{code.slug}').get('brl'))
            else:
                value = 0
            result = analyze_bitcoin(code.slug)
            data.append({"key":code.name, "value":value, "result":result})
        return render(request, self.template_name, {'content': data})
    
    def post(self, request, *args, **kwargs):
        # # Agende a execução da análise a cada 10 minutos.
        # schedule.every(10).minutes.do(analyze_bitcoin)
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)
        return render(request, self.template_name)
