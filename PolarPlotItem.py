import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class PolarPlotItem(pg.PlotItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAspectLocked(True)
        
        pen = pg.mkPen(color=(150, 150, 150, 153), width=1, style=QtCore.Qt.PenStyle.DashLine)
        self.angle_lines = []
        self.angle_labels = [] 
        for angle in range(0, 360, 30):
            line = pg.InfiniteLine(angle=angle, pen=pen)
            self.addItem(line)
            self.angle_lines.append(line)

        self.radial_lines = []
        self.radius_labels = [] 
        self.update_radial_grid()
        self.sigRangeChanged.connect(self.update_radial_grid)
        self.sigRangeChanged.connect(self.update_angle_labels)

    def get_step_size(self, max_radius):
        steps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
        step = max_radius / 5  
        factor = 10 ** np.floor(np.log10(step))
        normalized_step = step / factor
        closest_step = min(steps, key=lambda x: abs(x - normalized_step))
        return closest_step * factor

    def update_radial_grid(self):
        for line in self.radial_lines:
            self.removeItem(line)
        for label in self.radius_labels:
            self.removeItem(label)
        
        self.radial_lines = []
        self.radius_labels = []
        vb = self.getViewBox()
        view_range = vb.viewRange()
        x_range = view_range[0][1] - view_range[0][0]
        y_range = view_range[1][1] - view_range[1][0]
        max_radius = min(x_range, y_range) / 2
        step = self.get_step_size(max_radius)
        pen = pg.mkPen(color=(150, 150, 150, 153), width=1, style=QtCore.Qt.PenStyle.DashLine)
        current_radius = step
        while current_radius <= max_radius:
            theta = np.linspace(0, 2 * np.pi, 32)
            x = current_radius * np.cos(theta)
            y = current_radius * np.sin(theta)
            line = self.plot(x, y, pen=pen)
            self.radial_lines.append(line)
            
            label_text = f'{int(current_radius)}' if current_radius.is_integer() else f'{current_radius:.2f}'
            label = pg.TextItem(text=label_text, color=(200, 200, 255), anchor=(0.5, 0.5))
            label_angle_x = current_radius * np.cos(np.pi/4)
            label_angle_y = current_radius * np.sin(np.pi/4)
            label.setPos(label_angle_x, label_angle_y)
            self.addItem(label)
            self.radius_labels.append(label)

            current_radius += step

    def update_angle_labels(self):
        for label in self.angle_labels:
            self.removeItem(label)
        
        self.angle_labels = []
        vb = self.getViewBox()
        view_rect = vb.viewRect()
        max_radius = min(view_rect.width(), view_rect.height()) / 2.3

        for line, angle in zip(self.angle_lines, range(0, 360, 30)):
            theta = np.radians(angle)
            x = max_radius * np.cos(theta)
            y = max_radius * np.sin(theta)

            label = pg.TextItem(text=f'{angle}°', color=(150, 150, 150, 153), anchor=(0.5, 0.5))
            label.setPos(x, y)
            self.addItem(label)
            self.angle_labels.append(label)

    def plot_polar(self, r, theta, **kwargs):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return self.plot(x, y, **kwargs)

if __name__ == '__main__':
    app = pg.mkQApp()

    win = pg.GraphicsLayoutWidget(show=True, title="Polar Plot Example")
    polar_plot = PolarPlotItem()
    win.addItem(polar_plot)

    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.abs(np.sin(2 * theta) * 10)

    polar_plot.plot_polar(r, theta, pen='r')

    app.exec()
