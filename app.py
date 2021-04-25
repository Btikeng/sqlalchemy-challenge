{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "from matplotlib import style\n",
    "style.use('fivethirtyeight')\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Python SQL toolkit and Object Relational Mapperimport sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['measurement', 'station']"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# We can view all of the classes that automap found\n",
    "Base.classes.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2017-08-23\n"
     ]
    }
   ],
   "source": [
    "# Design a query to retrieve the last 12 months of precipitation data and plot the results\n",
    "\n",
    "# Calculate the date 1 year ago from from most recent date in database\n",
    "most_current_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()\n",
    "most_current_date = str(most_current_date)[2:-3]\n",
    "print(most_current_date)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2016-08-23\n"
     ]
    }
   ],
   "source": [
    "year_from_current = str(eval(most_current_date[0:4])-1) + most_current_date[4:]\n",
    "print(year_from_current)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>precipitation</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>date</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2016-08-23</th>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2016-08-23</th>\n",
       "      <td>0.15</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2016-08-23</th>\n",
       "      <td>0.05</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2016-08-23</th>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2016-08-23</th>\n",
       "      <td>0.02</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            precipitation\n",
       "date                     \n",
       "2016-08-23           0.00\n",
       "2016-08-23           0.15\n",
       "2016-08-23           0.05\n",
       "2016-08-23            NaN\n",
       "2016-08-23           0.02"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Perform a query to retrieve the data and precipitation scores & sort the dataframe by date\n",
    "last_12m_prcp = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date >= year_from_current).filter(Measurement.date <= most_current_date).order_by(Measurement.date).all()\n",
    "\n",
    "# Save the query results as a Pandas DataFrame and set the index to the date column  \n",
    "last_12_prcp_df = pd.DataFrame(data=last_12m_prcp)\n",
    "last_12_prcp_df.set_index(\"date\", inplace=True)\n",
    "last_12_prcp_df.rename(columns={\"prcp\": \"precipitation\"}, inplace=True)\n",
    "last_12_prcp_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Use Pandas Plotting with Matplotlib to plot the data & Rotate the xticks for the dates\n",
    "last_12_prcp_df.plot()\n",
    "plt.legend(loc=9)\n",
    "plt.savefig(\"precipitation_analysis.png\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>precipitation</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>2021.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>0.177279</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>0.461190</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>0.020000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>0.130000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>6.700000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       precipitation\n",
       "count    2021.000000\n",
       "mean        0.177279\n",
       "std         0.461190\n",
       "min         0.000000\n",
       "25%         0.000000\n",
       "50%         0.020000\n",
       "75%         0.130000\n",
       "max         6.700000"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use Pandas to calcualte the summary statistics for the precipitation data\n",
    "last_12_prcp_df.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(9)"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# How many stations are available in this dataset?\n",
    "stations = session.query(func.count(Station.station))\n",
    "station_count = stations[0]\n",
    "station_count"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "('USC00519281', 2772)\n",
      "('USC00519397', 2724)\n",
      "('USC00513117', 2709)\n",
      "('USC00519523', 2669)\n",
      "('USC00516128', 2612)\n",
      "('USC00514830', 2202)\n",
      "('USC00511918', 1979)\n",
      "('USC00517948', 1372)\n",
      "('USC00518838', 511)\n"
     ]
    }
   ],
   "source": [
    "# What are the most active stations?\n",
    "observations = session.query(Measurement.station, func.count(Measurement.tobs))\\\n",
    "             .group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc())\n",
    "\n",
    "for station in observations:\n",
    "    print(station)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[(54.0, 85.0, 71.66378066378067)]\n"
     ]
    }
   ],
   "source": [
    "# Using the station id from the previous query, calculate the lowest temperature recorded, highest temperature recorded, and average temperature most active station?\n",
    "top_station = observations[0][0]\n",
    "\n",
    "stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == top_station)\n",
    "                      \n",
    "stats_list=list(stats)\n",
    "print(stats_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    }
   },
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<Figure size 432x288 with 0 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "# Choose the station with the highest number of temperature observations.\n",
    "# Query the last 12 months of temperature observation data for this station and plot the results as a histogram\n",
    "\n",
    "tobs = session.query(Measurement.tobs)\\\n",
    ".filter(Measurement.date >= year_from_current)\\\n",
    ".filter(Measurement.date <= most_current_date)\\\n",
    ".filter(Measurement.station == top_station)\\\n",
    "\n",
    "tobs_list = []\n",
    "for tob in tobs:\n",
    "    tobs_list.append(tob[0])\n",
    "    \n",
    "fig = plt.figure()\n",
    "plt.hist(tobs_list, bins=12 , label='tobs')\n",
    "plt.ylabel(\"Frequency\")\n",
    "plt.legend(loc=1)\n",
    "plt.show()\n",
    "plt.savefig(\"station_observation_analysis.png\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[(62.0, 69.57142857142857, 74.0)]\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' \n",
    "# and return the minimum, average, and maximum temperatures for that range of dates\n",
    "\n",
    "# Define start and end date\n",
    "start_date = '2012-02-28'\n",
    "end_date = '2012-03-05'\n",
    "\n",
    "def calc_temps(start_date, end_date):\n",
    "    \"\"\"TMIN, TAVG, and TMAX for a list of dates.\n",
    "    \n",
    "    Args:\n",
    "        start_date (string): A date string in the format %Y-%m-%d\n",
    "        end_date (string): A date string in the format %Y-%m-%d\n",
    "        \n",
    "    Returns:\n",
    "        TMIN, TAVE, and TMAX\n",
    "    \"\"\"\n",
    "\n",
    "    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "print(calc_temps(start_date, end_date))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[(61.0, 69.75510204081633, 75.0)]\n"
     ]
    }
   ],
   "source": [
    "# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax \n",
    "# for your trip using the previous year's data for those same dates.\n",
    "\n",
    "prev_year_start = str(eval(start_date[0:4])-1) + start_date[4:]\n",
    "prev_year_end = str(eval(end_date[0:4])-1) + end_date[4:]\n",
    "\n",
    "last_year_temp_analysis = calc_temps(prev_year_start, prev_year_end)\n",
    "\n",
    "tmin = last_year_temp_analysis[0][0]\n",
    "tmax = last_year_temp_analysis[0][1]\n",
    "tavg = last_year_temp_analysis[0][2]\n",
    "\n",
    "print(last_year_temp_analysis)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAARAAAAIwCAYAAABOTjS+AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8vihELAAAACXBIWXMAAAsTAAALEwEAmpwYAAAhbklEQVR4nO3df3zO9f7H8efVSCynseba6ZgJqzWHMPkVuaVTOVY0dISI4mg6ThGh26lO4vg1RbUkDpMZlSjrp5vI78apHCrl1/GjsBkuJr/t+v7h5vpuNlxe7drnGo/77XZut7PP5/rxuliPfa7353OZy+PxeAUABlc5PQCA0ouAADAjIADMCAgAMwICwIyAADAjIKXIzJkzFRYWppkzZzo9CiBJKuP0AJe7sLCwS7p9SkqKunbtGphhLtHJkycVFxenvXv36u6779Z7773n9Eg+CQkJWrFihd+379y5syZOnBjAia5MBCTABg8eXGhbenq6du7cqc6dO6tatWoF9tWpU+e8j3Xffffptttuk9vtLvY5i/LRRx9p7969crlc+uKLL7Rjx45C8zqlS5cuat68eYFty5cv14oVK3T77bcX2nehP1fYubgSteSd/emZkZGhFi1aOD3OebVt21ZLly7VwIEDlZycrIEDB+of//iH02Od18iRIzV69GgNHjxYQ4cOdXqcKwJrIEEkISFBYWFh2rZtm1577TU1adJEbrdbXbp0kXT+NZA6deooLCxMx48f1/Dhw1W3bl1VqVJF9evX15gxY3TixIlLnmXr1q1atmyZmjRpogEDBqhixYpKS0vTqVOnfLfZtWuXKleurGbNmp33cR599FGFhYVpyZIlvm15eXl644031KhRI7ndbt1yyy0aNGiQDh486HstxS0rK0tDhgxRgwYN5Ha7FR0drcTExAJznXX2z3nkyJH69ttv1aFDB1WrVk3VqlVTt27d9PPPP0s682fUo0cP1axZU5GRkUpISND69esLPV5SUpLCwsK0bNkypaenq3nz5oqMjFRMTIz69eun7OzsYn+9JYWABKFnnnlGycnJqlu3rvr06aN69er5db8ePXpo5syZat26tXr16qW8vDz961//Uo8ePS55htTUVHm9XnXp0kUVKlTQAw88oD179ujTTz/13eaGG27QnXfeqR9++EFr164t9BgHDx7UJ598oqpVqxY40howYICeffZZHTp0SN27d1eHDh305ZdfKjExsUCgisv333+vFi1aaNKkSbrxxhvVu3dvJSQk6JtvvtEDDzygGTNmFHm/b7/9Vm3atFGZMmXUvXt31a5dWxkZGWrXrp1+/PFHtWrVSvv27VPnzp3VokULrVixQomJiTp8+HCRj/fGG2/o6aefVt26dZWUlKQaNWpoxowZuvfee7V///5if90lgTWQILR+/XotXbpU0dHRl3S/jRs3atWqVb6f4M8995wSEhL0ySefaM6cOerYsaNfj3PixAmlp6erQoUKSkxMlCR17dpVM2bM0PTp03X//ff7btu1a1d98cUXmjlzZqHQzZs3T8eOHdNDDz2kq64687Nq+fLlSk1NVY0aNbRo0SLfrM8//7zat2+v3bt3X9JrvpjTp0/rkUce0cGDB5WRkVFgbWTPnj266667NGjQIN17772qUqVKgfsuWLBA06dPV7t27SRJXq9XHTt21BdffKF77rlHQ4YMUd++fX23f/LJJzV9+nTNmDFDSUlJhWZZuHChFi5cqFtvvdW3bdCgQZo8ebKGDRum8ePHF+trLwkcgQShfv36XXI8pDPfjPkP/8uXL+9bs0hLS/P7cT766CPl5OSobdu2qlixoiSpSZMmqlWrlhYtWqTt27f7bpuQkKDrrrtO77//fqG3Sunp6ZLkewsmSbNnz5Yk9e/fv8CsV199tZ577jm/Z/TXggULtHnzZj322GOFFlYjIyPVr18/HTt2TB9++GGh+zZv3twXD0lyuVx68MEHJUnh4eGFItGpUydJKvJtzNn9+eMhSc8++6xCQ0P17rvv6uTJk5f+Ah3GEUgQatiwoel+t99+e6FtzZo1k8vl0rp16/x+nGnTpklSodPJXbp00bBhwzRjxgxfmMqVK6cOHTpo6tSp+uyzz9S2bVtJ0pYtW7R69Wo1bdpUNWrU8D3G2TmaNm1a6HkbNmyoMmXKFOvbmMzMTEnSzz//rJEjRxbav3XrVklnjt7OVbdu3ULbIiMjJUm1a9eWy+Uqct+uXbuKnKWov59KlSopLi5Oa9as0aZNmxQXF3ehlxN0CEgQOvdQ+rfc75prrlHFihV16NAhvx5jy5YtWr58uapVq1boJ/ZDDz2k4cOHKy0tTUOGDFGZMme+fbp27aqpU6cqPT3dF5BZs2ZJOnP9RX65ubmSpIiIiELPHRISosqVKxfrouLZtYX58+dr/vz5573dr7/+Wmjb2aOvc2e82L7zHUmc7+/17J+Fv39HwYSABKFzf7L5Kzs7W1FRUQW2HTt2TLm5uapUqZJfj3F28XTHjh3nvc+ePXv0ySef+GIRHx+v2NhYLVy4UHv37tX111+v2bNnF1hDOevsf3h79+7VddddV2Df6dOni30x8Xe/+50k6e233/bN65TzhXHv3r2S/n/W0oQ1kMtIUVdmrly5Ul6vt8jD8XOdOHFCs2bNksvlUteuXdWtW7dC/2vTpo0kafr06QXu27lzZ506dUrvvvuuli5dqp9//ln33XdfoZ/UZ+dYtWpVoef/z3/+U+xnYW677bbzPl9JK+rvx+Px6IcfflCFChUUExPjwFS/DUcgl5GxY8eqdevWvsXJo0ePavjw4ZIKr2cUJSMjQzk5ObrjjjuUkpJS5G1Onjyp2rVr+xZTzy72durUScOGDVN6err++Mc/nvc5H3roIaWlpemVV17R/fff75v15MmTeumlly71JV9UmzZtVKNGDU2bNk0tWrTwBTC///73v4qKilLlypWL/fnze+edd9S7d+8CC6kjRozQr7/+qkceeURly5YN6PMHAgG5jNx8881q2rSp2rZtqzJlyujjjz/Wtm3b1KZNG79O4aampkrSBa8bKVu2rLp06aLx48fr7bff9p05iYyM1F133aUFCxZo48aNha79OKt58+bq0aOHUlNT1bRpU91///0qV66cPvvsM1WsWFG///3vtWfPHtPrP9+8aWlpat++vbp06aKGDRvq1ltvVWhoqH755RetW7dOmzZt0tKlSwMekLvvvlutW7dWYmKi3G63Vq5cqczMTFWvXl3PP/98QJ87UHgLcxmZNm2aunTpok8++USTJ0+W1+vV0KFDlZqaetF1lbOLp+Hh4brvvvsueNvu3bvL5XIVujL17BHHyZMnC1z7ca6XX35ZI0aM0LXXXqvU1FS99957atmypebNm6fc3NxiXwuIi4vTihUrNHDgQB05ckSzZs3S5MmT9fXXX6tmzZp69dVXS+TtQ1JSksaNG6d169Zp4sSJ2rJlix5++GEtWLBA4eHhAX/+QOCzMJeBOnXqaOfOnfJ4PE6P8pts2bJF8fHxatSokRYsWOD0OMUmKSlJs2bNCvrPPllwBIISl52drby8vALbjhw54vsAnNNnS+A/1kBQ4t566y3Nnj3b96GyrKwsLV26VL/88osaNGig3r17Oz0i/ERAUOJatmyp7777TsuWLdO+ffvkcrl04403qlu3burXr5/KlSvn9IjwE2sgAMxYAwFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGaOBeT06dMaPny46tatK7fbrbp162r48OE6deqU7zZer1cjR45UbGysIiMjlZCQoA0bNjg1MoBzOBaQ8ePHa8qUKRo9erRWr16tUaNGafLkyXr55Zd9t5kwYYJSUlI0evRoLVq0SBEREUpMTFRubq5TYwPIx+XxeLxOPHGnTp1UqVIlvfnmm75tjz/+uA4cOKB33nlHXq9XsbGx6t27twYOHChJOnr0qGJiYvTSSy+pZ8+eTowNIB/HjkCaNGmi5cuXa+PGjZKkH3/8UcuWLdPdd98tSdq+fbuysrLUqlUr333Kly+vZs2aKTMz05GZARRUxqknfuqpp3T48GE1btxYISEhOnXqlAYOHKhevXpJkrKysiRJERERBe4XERGh3bt3n/dxN23aFLihgStMTEzMBfc7FpC5c+dq9uzZmjJlimJjY7V+/XoNGTJE1apVU/fu3X23c7lcBe7n9XoLbcvvYi8YQPFxLCDPP/+8/va3v6lDhw6SpNq1a2vnzp165ZVX1L17d7ndbklSdna2qlat6rtfTk5OoaMSAM5wbA3kyJEjCgkJKbAtJCREeXl5kqTo6Gi53W4tXrzYt//YsWNatWqVGjduXKKzAiiaY0cgrVu31vjx4xUdHa3Y2FitW7dOKSkpeuihhySdeeuSlJSkcePGKSYmRrVq1VJycrJCQ0PVsWNHp8YGkI9jp3Fzc3M1YsQIffTRR8rJyZHb7VaHDh30zDPP6JprrpF0Zr1j1KhRSk1NlcfjUXx8vJKTkxUXF+fEyADO4VhAAJR+fBYGgJljayC4MoWFhRX42uPxODIHigdHIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwIyAADAjIADMCAgAMwICwKyM0wNcDsqtmuf0CKUWf3b+Od400ekRisQRCAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCMgAMwICAAzAgLAjIAAMCvj9AC4shz9dJrTI6AYOXoEsmfPHj3++OOqWbOm3G63GjdurOXLl/v2e71ejRw5UrGxsYqMjFRCQoI2bNjg4MQA8nMsIB6PR/fee6+8Xq/effddZWZmasyYMYqIiPDdZsKECUpJSdHo0aO1aNEiRUREKDExUbm5uU6NDSAfx97CvPrqq4qMjNSkSZN826pXr+77/16vVxMnTtRTTz2ldu3aSZImTpyomJgYzZkzRz179izpkQGcw7EjkI8//ljx8fHq2bOnatWqpebNm+utt96S1+uVJG3fvl1ZWVlq1aqV7z7ly5dXs2bNlJmZ6dTYAPJxLCDbtm3Tv//9b1WvXl3vv/++Hn/8cb344ouaPHmyJCkrK0uSCrylOft1dnZ2ic8LoDDH3sLk5eWpfv36euGFFyRJt956q7Zu3aopU6bor3/9q+92LperwP28Xm+hbflt2rQpMANfwA379pf4c+LKssuB72tJiomJueB+xwLidrt18803F9h200036eeff/btl6Ts7GxVrVrVd5ucnJxCRyX5XewFB0K5nO9K/DlxZQl14PvaH469hWnSpIk2b95cYNvmzZsVFRUlSYqOjpbb7dbixYt9+48dO6ZVq1apcePGJTorgKI5FpC+fftqzZo1Sk5O1tatW/XBBx/orbfeUq9evSSdeeuSlJSk8ePHa/78+frhhx/Ut29fhYaGqmPHjk6NDSAfl8fj8Tr15J9//rmGDRumzZs3q2rVqurdu7f69OnjW+Pwer0aNWqUUlNT5fF4FB8fr+TkZMXFxTk1cpHKrZrn9Ai4zB1vmuj0CEVyNCCXCwKCQAvWgPBhOgBmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAGQEBYEZAAJgREABmBASAWRl/b7hv3z599dVX2rhxo/bt2yeXy6Xw8HDddNNNaty4scLDwwM5J4AgdMGAHD9+XO+9955mzpypzMxMeb3eIm/ncrnUqFEjde3aVX/5y19Urly5gAwLILi4PB5PkVWYNm2axo4dq5ycHN15551q2bKlGjRooOrVq6tSpUryer3yeDz63//+p6+//lpLlizRkiVLdP3112vQoEHq2bNnSb8Wx5RbNc/pEXCZO9400ekRinTegMTFxSkpKUndunVTWFiYXw/m8Xg0Y8YMvfnmm/r++++Lc86gRkAQaKUuICdPnlTZsmVND/pb7lsaERAEWrAG5LxnYX5LAK6keABXsguexp0wYYJ++umnkpoFQClzwYD885//1Lp163xfHzhwQFFRUVqxYkXABwMQ/C7pQjKv16vDhw/r1KlTgZoHQCnClagAzAgIALOLXsqem5urvXv3SpL2798vSTp48KBv27kiIiKKcTwAwey814FIUqVKleRyuQps83q9hbbldzYyVxKuA0GgBet1IBc8Ahk8eHBJzQGgFLrgEQj8wxEIAi1Yj0BYRAVgdt6ALFmyxPygX375pfm+AEqP8wakc+fO+tOf/qRZs2bp0KFDF32ggwcPKi0tTa1atVLXrl2LdUgAwem8i6jffPONxo4dq/79+6t///6qX7++6tWrp+joaIWFhfn+PZDt27dr7dq1Wrt2rbxerx5++GHNmjWrJF8DAIdcdBHV4/HonXfe0ccff6yvv/5aR44cKbA/NDRUDRo0UJs2bdSpUydVqlQpoAMHIxZREWjBuoh6SWdhTp8+rZ07d/qu9ahcubKioqIUEhISsAFLAwKCQAvWgPj9jypLUkhIiKpXr67q1asHaBwApQmncQGYERAAZgQEgBkBAWBGQACYERAAZpd0Gtfj8ej111/XggULtHPnTklSVFSU7rnnHj3xxBNX5EVkwJXM7wvJNm/erLZt22r37t265ZZbVLNmTXm9Xm3dulUbNmxQZGSk5s+fr5iYmEDPHHS4kAyBVuovJBs0aJAOHz6sDz/8UHfccUeBfUuWLFG3bt00ePBgzZ07t9iHBBCc/F4DyczM1OOPP14oHpLUsmVL9enTR1999VWxDgcguPkdkOuuu+6Cv2Q7LCzM71/CDeDy4HdAunXrprS0NOXm5hbad/bfAunWrVuxDgcguPm9BhITEyOXy6WGDRuqc+fOqlGjhiRpy5Ytmj17tiIiIhQTE6N58wouKCYmBufiD4Dfzu+zMP6conW5XPJ6vQW+vhJ+zQNnYRBopf4sTEZGRiDnAFAK+R2Q5s2bB3IOAKUQl7IDMLukS9nXr1+vtLQ0bdu2TR6Pp8B6h3RmzePzzz8v1gEBBC+/A5KamqoBAwboqquu0h/+8Af97ne/C+RcAEoBvwMyZswY1atXT+np6YqMjAzkTABKCb/XQA4dOqSHH36YeADw8TsgTZo00ZYtWwI5C4BSxu+AjB49WhkZGUpPT9fp06cDOROAUuKSfrHU22+/rf79+yskJERVqlQp9AulXC6X1q5dW9wzBj2uREWglforUVNSUvTcc8/p2muvVWxsLGdhAPgfkNdee0233367Zs+erdDQ0EDOBKCU8HsN5Ndff1X79u2JBwAfvwPSokULrVu3LpCzAChl/A7IuHHjtHr1ao0bN07Z2dmBnAlAKeH3WZjIyEh5vV6dPHlSklS2bFlddVXB/rhcLu3atav4pwxynIVBoJX6szCJiYlyuVyBnAVAKeN3QCZOnBjIOQCUQvx7IADMLikgO3bs0N///nfVq1dPUVFRWr58uSRp3759evrpp6/Iq1CBK5nfb2F++ukntW7dWnl5eWrYsKF27Njh+0xMeHi41qxZo+PHj+v1118P2LAAgovfAXnhhRdUsWJFLVy4UCEhIapVq1aB/ffcc48++OCD4p4PQBDz+y3MypUr1atXL1WpUqXIszFRUVHavXt3sQ4HILj5HZBTp05d8DL2AwcOFPp0LoDLm98BiYuL07Jly4rc5/V6lZGRoXr16hXXXABKgQsGZNasWdq+fbskKSkpSR9++KHGjBnj+21zeXl52rhxox599FF9++236tevX+AnBhA0Lngpe+XKlTVp0iQ9+OCDkqTx48drxIgROn36tLxer28tJCQkRC+++KL69u1bMlMHGS5lR6CVykvZz/29L0899ZQ6duyo+fPna+vWrcrLy9ONN96otm3bKjo6OqCDAgg+l/SLpSSpatWqV+yRBoCCLrqIygfoAJzPBddAKlWqpKuvvrrQx/bP+2B8nB8IiFK5BiJJ8fHxql69egmMAqC0uWhAevbs6TsLAwD5Bc3H+ceNG6ewsDANGjTIt83r9WrkyJGKjY1VZGSkEhIStGHDBgenBJBfUARkzZo1mj59umrXrl1g+4QJE5SSkqLRo0dr0aJFioiIUGJionJzcx2aFEB+jgfk4MGD6t27t1577TWFhYX5tnu9Xk2cOFFPPfWU2rVrp7i4OE2cOFGHDx/WnDlznBsYgM8FA3LgwIGAr3+cDUTLli0LbN++fbuysrLUqlUr37by5curWbNmyszMDOhMAPxzyReSFafp06dr69atmjRpUqF9WVlZkqSIiIgC2yMiIi74zwZs2rSpeIf0ww379pf4c+LKssuB72tJiomJueB+xwKyadMmDRs2TJ9++qmuvvrq897u3AvZ8n8GpygXe8GBUC7nuxJ/TlxZQh34vvaHY2sgq1ev1r59+9S0aVOFh4crPDxcK1as0JQpUxQeHq7KlStLUqFfYpWTk1PoqASAMxw7AklISFD9+vULbHviiSdUs2ZNDRgwQLVq1ZLb7dbixYvVoEEDSdKxY8e0atUqDRs2zImRAZzDsYCEhYUVOOsiSRUqVFClSpUUFxcn6cy/QTJu3DjFxMSoVq1aSk5OVmhoqDp27OjAxADO5egi6sU8+eSTOnr0qAYNGiSPx6P4+HjNnTtXFStWdHo0ALqE342L8+PDdAi0YP0wneMXkgEovQgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzAgIADPHAvLyyy/rzjvvVFRUlGrWrKlOnTrphx9+KHAbr9erkSNHKjY2VpGRkUpISNCGDRscmhjAuRwLyPLly/XYY4/p888/1/z581WmTBk98MADOnDggO82EyZMUEpKikaPHq1FixYpIiJCiYmJys3NdWpsAPm4PB6P1+khJOnw4cOqVq2aZs6cqT//+c/yer2KjY1V7969NXDgQEnS0aNHFRMTo5deekk9e/Z0eOL/V27VPKdHwGXueNNEp0coUtCsgRw+fFh5eXkKCwuTJG3fvl1ZWVlq1aqV7zbly5dXs2bNlJmZ6dCUAPILmoAMGTJEderUUaNGjSRJWVlZkqSIiIgCt4uIiFB2dnaJzwegsDJODyBJzz77rL766it99tlnCgkJKbDP5XIV+Nrr9Rbalt+mTZsCMuOF3LBvf4k/J64suxz4vpakmJiYC+53PCBDhw7V3LlzlZGRoerVq/u2u91uSVJ2draqVq3q256Tk1PoqCS/i73gQCiX812JPyeuLKEOfF/7w9G3MIMHD9acOXM0f/583XTTTQX2RUdHy+12a/Hixb5tx44d06pVq9S4ceOSHhVAERw7Ahk4cKDeeecdpaWlKSwszLfmERoaqmuvvVYul0tJSUkaN26cYmJiVKtWLSUnJys0NFQdO3Z0amwA+Th2Gvfs2ZZzDR48WEOHDpV0Zr1j1KhRSk1NlcfjUXx8vJKTkxUXF1eCk14cp3ERaMF6GjdorgMpzQgIAi1YAxI0p3EBlD4EBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgRkAAmBEQAGYEBIAZAQFgVioCMmXKFNWtW1dut1stW7bUypUrnR4JgEpBQObOnashQ4bo6aef1tKlS9WoUSM9+OCD2rlzp9OjAVe8oA9ISkqKunTpokceeUQ333yzxo4dK7fbralTpzo9GnDFK+P0ABdy4sQJrV27Vv369SuwvVWrVsrMzHRoqsKON010egTAEUF9BLJv3z6dPn1aERERBbZHREQoOzvboakAnBXUATnL5XIV+Nrr9RbaBqDkBXVAwsPDFRISUuhoIycnp9BRCYCSF9QBufrqq1WvXj0tXry4wPbFixercePGDk0F4KygXkSVpCeeeEJ9+vRRfHy8GjdurKlTp2rPnj3q2bOn06MBV7ygD0j79u21f/9+jR07VllZWbrlllv07rvvqlq1ak6PBlzxXB6Px+v0EABKp6BeAwEQ3AgIADMCAsCMgAAwIyAAzAgIADMCAsCMgAAwIyAAzP4PU8znsYdbO1QAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 288x576 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Plot the results from your previous query as a bar chart. \n",
    "# Use \"Trip Avg Temp\" as your Title\n",
    "# Use the average temperature for the y value\n",
    "# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=plt.figaspect(2.))\n",
    "\n",
    "bar= ax.bar(1, tmax, yerr=(tmax-tmin),alpha=0.5, color=\"coral\")\n",
    "ax.set(xticks=range(1), xticklabels=\"a\", title=\"Trip Avg Temp\", ylabel = \"Temp (F)\")\n",
    "ax.margins(.2,.2)\n",
    "fig.tight_layout()\n",
    "\n",
    "plt.savefig(\"temperature_analysis.png\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
