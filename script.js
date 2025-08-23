document.addEventListener('DOMContentLoaded', () => {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const statusMessage = document.getElementById('status-message');
    const occupancyChartCanvas = document.getElementById('occupancyChart');

    let occupancyChart;

    // Função para buscar dados de ocupação do backend
    async function fetchOccupancyData() {
        try {
            const response = await fetch('https://gymnow-7c3f669b80bd.herokuapp.com/api/occupancy');
            const data = await response.json();
            
            // Pegar o último registro de ocupação
            if (data && data.length > 0) {
                const latestRecord = data[data.length - 1];
                updateStatus(latestRecord.unique_devices);
            } else {
                updateStatus(0); // Nenhuma ocupação se não houver dados
            }
        } catch (error) {
            console.error('Erro ao buscar dados de ocupação:', error);
            updateStatus(-1); // Indicar erro
        }
    }

    // Função para atualizar o status visual
    function updateStatus(uniqueDevices) {
        let status = '';
        let message = '';
        let className = '';

        if (uniqueDevices === -1) {
            status = 'Erro';
            message = 'Não foi possível conectar ao servidor.';
            className = 'full'; // Usar vermelho para erro
        } else if (uniqueDevices <= 3) { // Exemplo de limites, ajustar conforme a capacidade real
            status = 'Vazia';
            message = 'Ótimo para treinar! Poucas pessoas.';
            className = 'empty';
        } else if (uniqueDevices <= 7) {
            status = 'Moderada';
            message = 'Movimento normal. Bons treinos!';
            className = 'moderate';
        } else {
            status = 'Cheia';
            message = 'Pode haver espera para equipamentos. Academia movimentada!';
            className = 'full';
        }

        statusText.textContent = `Academia: ${status}`;
        statusMessage.textContent = message;
        statusIndicator.className = `status-indicator ${className}`;
    }

    // Função para simular e renderizar o gráfico de horários de pico
    function renderPeakHoursChart() {
        const labels = ['06h', '07h', '08h', '09h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h'];
        // Dados simulados de ocupação média por hora
        const data = [3, 5, 8, 7, 6, 4, 5, 7, 8, 9, 10, 12, 15, 18, 20, 16, 10, 5]; 

        if (occupancyChart) {
            occupancyChart.destroy(); // Destruir gráfico existente antes de criar um novo
        }

        occupancyChart = new Chart(occupancyChartCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ocupação Média (Simulado)',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Nível de Ocupação'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Hora do Dia'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Chamar as funções inicialmente
    fetchOccupancyData();
    renderPeakHoursChart();

    // Atualizar dados a cada 10 segundos
    setInterval(fetchOccupancyData, 10000);
});
