import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
import os

class SebraeControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Gastos - Sebrae")
        ctk.set_appearance_mode("Dark")  # 'Light' ou 'Dark'
        ctk.set_default_color_theme("blue")  # 'green', 'dark-blue', etc.

        # Dados iniciais
        self.data = pd.DataFrame(columns=['NOMESOLICITANTE', 'CH_ESTIMADA', 'PORTFOLIO', 'NOMEABREVFANTASIA',
                                          'DATAINIEXEC', 'CONTRATO_SGF', 'PROJETO', 'ACAO', 'VALORTOTAL', 'FORNECEDOR', 'NOMEUNIDADE', 'STATUSPROCESSO'])

        # Frames e Layout
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Botões e Labels
        ctk.CTkLabel(self.frame, text="Controle de Gastos", font=("Arial", 18)).pack(pady=10)

        self.import_button = ctk.CTkButton(self.frame, text="Importar Planilha", command=self.import_xlsx)
        self.import_button.pack(pady=5)

        self.process_button = ctk.CTkButton(self.frame, text="Processar Dados", command=self.process_data)
        self.process_button.pack(pady=5)

        self.add_button = ctk.CTkButton(self.frame, text="Adicionar Dados", command=self.add_data)
        self.add_button.pack(pady=5)

        self.view_button = ctk.CTkButton(self.frame, text="Visualizar Dados", command=self.view_data)
        self.view_button.pack(pady=5)

    def import_xlsx(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if filepath:
            try:
                loading = ctk.CTkLabel(self.frame, text="Carregando... Aguarde.", font=("Arial", 12))
                loading.pack(pady=5)
                self.root.update()  # Atualiza a interface

                # Importa os dados
                all_sheets = pd.ExcelFile(filepath)
                combined_data = pd.DataFrame()
                expected_columns = ['NOMESOLICITANTE', 'CH_ESTIMADA', 'PORTFOLIO', 'NOMEABREVFANTASIA',
                                    'DATAINIEXEC', 'CONTRATO_SGF', 'PROJETO', 'ACAO', 'VALORTOTAL', 'FORNECEDOR', 'NOMEUNIDADE', 'STATUSPROCESSO', 'TIPODEMANDA']
                for sheet in all_sheets.sheet_names:
                    temp_data = pd.read_excel(all_sheets, sheet_name=sheet)
                    if not all(col in temp_data.columns for col in expected_columns):
                        messagebox.showerror("Erro", f"A aba {sheet} não contém as colunas esperadas.")
                        loading.destroy()
                        return
                    temp_data = temp_data[expected_columns]
                    combined_data = pd.concat([combined_data, temp_data], ignore_index=True)
                self.data = combined_data
                loading.destroy()
                messagebox.showinfo("Sucesso", f"Arquivo importado com sucesso: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar o arquivo: {str(e)}")

    def process_data(self):
        if self.data.empty:
            messagebox.showerror("Erro", "Nenhum dado disponível para processar!")
            return
        try:
            # Processamento
            self.data['VALORTOTAL'] = pd.to_numeric(self.data['VALORTOTAL'], errors='coerce').fillna(0)

            filtered_data = self.data[
                (self.data['CONTRATO_SGF'].notna()) &
                (self.data['TIPODEMANDA'].isin(['CONSULTORIA GESTÃO', 'CAPACITAÇÃO', 'SEBRAETEC'])) &
                (self.data['NOMEUNIDADE'] == '1.01.2.44 - ESCRITORIO REGIONAL METROPOLITANO DE FORTALEZA') &
                (self.data['STATUSPROCESSO'] != 'CANCELADO')
            ]

            filtered_data['VALORTOTAL_FORMATADO'] = filtered_data['VALORTOTAL'].apply(lambda x: f"R$ {x:,.2f}")

            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                title="Salvar Resultados"
            )
            if save_path:
                filtered_data.to_excel(save_path, index=False)
                messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar os dados: {str(e)}")

    def add_data(self):
        # Interface com entrada de dados manual
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Adicionar Dados")

        entries = {}
        for idx, col in enumerate(self.data.columns):
            ctk.CTkLabel(add_window, text=col).grid(row=idx, column=0, padx=10, pady=5)
            entries[col] = ctk.CTkEntry(add_window)
            entries[col].grid(row=idx, column=1, padx=10, pady=5)

        def save_data():
            new_data = {col: entries[col].get() for col in self.data.columns}
            new_row = pd.DataFrame([new_data])
            self.data = pd.concat([self.data, new_row], ignore_index=True)
            messagebox.showinfo("Sucesso", "Novo dado adicionado!")
            add_window.destroy()

        ctk.CTkButton(add_window, text="Salvar", command=save_data).grid(row=len(self.data.columns), columnspan=2, pady=10)

    def view_data(self):
        view_window = ctk.CTkToplevel(self.root)
        view_window.title("Visualizar Dados")
        text_box = ctk.CTkTextbox(view_window, width=600, height=400)
        text_box.pack(pady=10, padx=10)
        text_box.insert("1.0", self.data.to_string(index=False))

if __name__ == "__main__":
    root = ctk.CTk()
    app = SebraeControlApp(root)
    root.mainloop()
