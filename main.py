import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import numpy as np

class MatrixCalculatorApp(App):
    def build(self):
        # Main layout
        layout_utama = BoxLayout(orientasi='vertical', padding=10, spasi=10)
        
        # Ordo (Matrix Size) Selection
        ordo_layout = BoxLayout(size_hint_y=None, tinggi=50)
        ordo_label = Label(text="Pilih Ordo Matriks:", size_hint_x=0.4)
        self.ordo_spinner = Spinner(
            text='3',
            values=('2', '3', '4', '5', '6', '7'),
            size_hint_x=0.6
        )
        self.ordo_spinner.bind(text=self.update_matrix_grids)
        ordo_layout.add_widget(ordo_label)
        ordo_layout.add_widget(self.ordo_spinner)
        layout_utama.add_widget(ordo_layout)
        
        # Scrollable container for matrices
        scroll_view = ScrollView()
        scroll_layout = BoxLayout(orientasi='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('tinggi'))
        
        # Matrix 1 Container
        matrix1_label = Label(text="Matriks 1", size_hint_y=None, tinggi=40)
        scroll_layout.add_widget(matrix1_label)
        
        self.matrix1_grid = GridLayout(
            cols=int(self.ordo_spinner.text), 
            size_hint_y=None, 
            tinggi=50 * int(self.ordo_spinner.text)
        )
        self.matrix1_inputs = []
        self._create_matrix_inputs(self.matrix1_grid, self.matrix1_inputs)
        scroll_layout.add_widget(self.matrix1_grid)
        
        # Operation Selection
        operasi_layout = BoxLayout(size_hint_y=None, tinggi=50)
        operasi_label = Label(text="Pilih Operasi:", size_hint_x=0.4)
        self.operasi_spinner = Spinner(
            text='Penjumlahan',
            values=('Penjumlahan', 'Pengurangan', 'Perkalian', 'Transpose', 'Determinan'),
            size_hint_x=0.6
        )
        self.operasi_spinner.bind(text=self.update_matrix_grids)
        operasi_layout.add_widget(operasi_label)
        operasi_layout.add_widget(self.operasi_spinner)
        scroll_layout.add_widget(operasi_layout)
        
        # Matrix 2 Container (for operations needing two matrices)
        matrix2_label = Label(text="Matriks 2", size_hint_y=None, tinggi=40)
        scroll_layout.add_widget(matrix2_label)
        
        self.matrix2_grid = GridLayout(
            cols=int(self.ordo_spinner.text), 
            size_hint_y=None, 
            tinggi=50 * int(self.ordo_spinner.text)
        )
        self.matrix2_inputs = []
        self._create_matrix_inputs(self.matrix2_grid, self.matrix2_inputs)
        scroll_layout.add_widget(self.matrix2_grid)
        
        # Calculate Button
        calculate_btn = Button(text="Hitung", size_hint_y=None, tinggi=50)
        calculate_btn.bind(on_press=self.hitung_matriks)
        scroll_layout.add_widget(calculate_btn)
        
        # Result Area
        self.result_label = Label(
            text="Hasil akan ditampilkan di sini", 
            size_hint_y=None, 
            tinggi=100,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        scroll_layout.add_widget(self.result_label)
        
        scroll_view.add_widget(scroll_layout)
        layout_utama.add_widget(scroll_view)
        
        returnlayout_utama
    
    def _create_matrix_inputs(self, grid, input_list):
        grid.clear_widgets()
        input_list.clear()
        ordo = int(self.ordo_spinner.text)
        grid.cols = ordo
        grid.size_hint_y = None
        grid.tinggi = 50 * ordo
        
        for _ in range(ordo):
            row_inputs = []
            for _ in range(ordo):
                text_input = TextInput(
                    multiline=False, 
                    input_type='number', 
                    size_hint=(1, None), 
                    tinggi=40
                )
                grid.add_widget(text_input)
                row_inputs.append(text_input)
            input_list.append(row_inputs)
    
    def update_matrix_grids(self, *args):
        # Update both matrix grids when ordo or operation changes
        self._create_matrix_inputs(self.matrix1_grid, self.matrix1_inputs)
        
        # Show/hide second matrix based on operation
        operasi = self.operasi_spinner.text
        if operasi in ["Penjumlahan", "Pengurangan", "Perkalian"]:
            self._create_matrix_inputs(self.matrix2_grid, self.matrix2_inputs)
            self.matrix2_grid.opacity = 1
        else:
            self.matrix2_grid.clear_widgets()
            self.matrix2_grid.opacity = 0
    
    def get_matrix_values(self, inputs):
        try:
            return [[float(inp.text) if inp.text else 0 for inp in row] for row in inputs]
        except ValueError:
            self.result_label.text = "Error: Masukkan hanya angka!"
            return None
    
    def hitung_matriks(self, *args):
        matriks1 = self.get_matrix_values(self.matrix1_inputs)
        operasi = self.operasi_spinner.text
        
        if matriks1 is not None:
            try:
                if operasi in ["Penjumlahan", "Pengurangan", "Perkalian"]:
                    matriks2 = self.get_matrix_values(self.matrix2_inputs)
                    if matriks2 is None:
                        return
                    
                    if operasi == "Penjumlahan":
                        hasil = np.add(matriks1, matriks2)
                    elif operasi == "Pengurangan":
                        hasil = np.subtract(matriks1, matriks2)
                    elif operasi == "Perkalian":
                        hasil = np.matmul(matriks1, matriks2)
                    
                    self.result_label.text = f"Hasil {operasi} Matriks:\n{hasil}"
                
                elif operasi == "Transpose":
                    hasil = np.transpose(matriks1)
                    self.result_label.text = f"Transpose Matriks:\n{hasil}"
                
                elif operasi == "Determinan":
                    hasil = np.linalg.det(matriks1)
                    self.result_label.text = f"Determinan Matriks: {hasil}"
            
            except Exception as e:
                self.result_label.text = f"Error: {str(e)}"

def main():
    MatrixCalculatorApp().run()

if __name__ == '__main__':
    main()
